__author__ = 'Timo Boldt'
__version__ = '1.0.0'

import time
import lib.Zlib as Zlib


class Server:

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
        self.__logger.log("create server instance", "debug")
        # create an instance of Zserver
        if self.__host and self.__port:
            self.__app = Zlib.Zlib(self.__host, self.__port)
            self.__app.set_logger(self.__logger)
            try:
                self.__app.server()
            except Exception as e:
                print(e)

    def run(self, data, run_event):
        while run_event.is_set():
            try:
                # send response to client
                self.__app.send(data)
            except Exception as e:
                pass
            time.sleep(self.__sleep_interval)


def worker(data, logger, config, run_event):
    obj = Server(data, logger, config)
    obj.run(data, run_event)
