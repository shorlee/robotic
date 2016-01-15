__author__ = 'Timo Boldt'
__version__ = '1.0.0'

import time
import lib.Zlib as Zlib


class Client:

    def __init__(self, data, logger, config):
        # get global data
        self.__data = data

        # load configuration
        self.__config = config.get_config()
        self.__config_network = config.get_network()

        # set logging options and create logger
        self.__logger = logger

        # wait length (time.sleep(x))
        self.__sleep_interval = float(self.__config_network["interval"])

        # networking options
        self.__host = self.__config_network["host"]
        self.__port = self.__config_network["port"]

        # server instance (will be instantiated in start)
        self.__app = None

        # lets prepare our server instance
        self.__prepare()

    def __prepare(self):
        # create instance of ZeroMQ Server with defined configuration
        self.__logger.log("creating client instance", "debug")
        # create an instance of Zserver
        if self.__host and self.__port:
            self.__app = Zlib.Zlib(self.__host, self.__port)
            self.__app.set_logger(self.__logger)
            try:
                self.__app.client()
            except Exception as e:
                print(e)

    def run(self, run_event):
        # run loop
        while run_event.is_set():
            response = None
            # to keep safe, that we get an answer first, before we will send a new message ...
            while not response:
                # we must try catch this, otherwise we will get Exceptions from zmq if recv was not successful
                try:
                    # try to recieve response, otherwise wait, and retry
                    response = self.__app.recv()
                    # nothing to do with Exceptions so far
                except Exception as e:
                    self.__logger.log(e)
                    time.sleep(self.__sleep_interval)
                    pass

            for key in response:
                self.__data[key] = response[key]
            time.sleep(self.__sleep_interval)


# working function for spawning process (multiprocessing)
def worker(data, logger, config, run_event):
    c = Client(data, logger, config)
    c.run(run_event)
