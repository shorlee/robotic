from threading import Thread, Event

import argparse
import importlib
import libraries.Config as Config
import libraries.Logger as Logger
from time import sleep
import sys

def load_class(full_class_string):
    """
    load classes dynamicly by full class address
    :param full_class_string:
    :return:
    """
    class_data = full_class_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)
    __import__(module_path + "." + class_str)
    return getattr(module, class_str)


"""
Die Roboter-Klasse wird vom Master geladen und wird in Verbindung mit einer Client-Instanz gestartet:

python master_thread.py -m Robo Client

Das Robo-Modul muss eine Funktion worker(data, logger) enthalten.
Hierbei ist data das unten stehende Array und logger eine Instanz von logging die das printen und loggen von
Nachrichten und Werten ermöglicht.

Beispiel:

def worker(data, logger):
    while True:
        do_something(data["axis_x"])
        logger.log("Nachricht zum loggen", "debug")

Die verwendeten Werte:
        data["axis"]["x"]           X Wert
        data["axis"]["y"]           Y Wert
        data["axis"]["angle"]       Winkel in Grad
        data["axis"]["radiant"]     Winkel in Radiant
        data["axis"]["speed"]       Geschwindigkeit
        data["ctrl"]["connected"]   USB Controller verbunden?
        data["ctrl"]["mode"]        Bewegungsmodus (
"""


def main():
    # all threads in dict to get better controlling
    threads = dict()

    # make sure threads are killed by signal
    run_event = Event()
    run_event.set()

    ########################################
    # argument parsing via argparser
    ########################################
    parser = argparse.ArgumentParser(description='starting robot procs')
    parser.add_argument('-m', '--modules', nargs='+', help='modules to load', required=True, dest="modules")
    parser.add_argument('-c', '--config', help='configuration file', required=False, default="server.ini",
                        dest="configfile")
    args = parser.parse_args()

    ########################################
    # configuration parameters (global config)
    ########################################
    g_config = Config.Config(args.configfile)
    config_logging = g_config.get_logging()
    sleep_timer = g_config.get_network()['interval']

    ########################################
    # logger parameters
    ########################################
    logger = Logger.Logger(config_logging["log_level"],
                           config_logging["log_file"],
                           Config.get_bool(config_logging["log_print"]),
                           Config.get_bool(config_logging["log_syslog"]))

    ########################################
    # shared data
    ########################################
    shared_data = dict()

    shared_data["axis"] = dict()
    shared_data["ctrl"] = dict()
    shared_data["signal"] = dict()

    shared_data["axis"]["x"] = 0.0
    shared_data["axis"]["y"] = 0.0
    shared_data["axis"]["angle"] = 0.0
    shared_data["axis"]["speed"] = 0.0
    shared_data["axis"]["radiant"] = 0.0
    shared_data["ctrl"]["connected"] = False
    shared_data["ctrl"]["mode"] = None
    shared_data["ctrl"]["height"] = False
    shared_data["signal"]["terminate"] = False

    # load all modules that are passed by argparser
    for mod in args.modules:
        c = load_class("modules." + mod)
        threads[mod] = Thread(target=c.worker, args=[shared_data, logger, g_config, run_event])

    # start threads
    for proc in threads:
        threads[proc].start()

    # keep the main application running
    try:
        # check for terminate signal by controller
        while True:
            if shared_data["signal"]["terminate"]:
                # let other processes do their work (pushing data to client e.g.)
                sleep(float(sleep_timer) + 1.0)
                run_event.clear()
                for proc in threads:
                    threads[proc].join()

                return 0

            sleep(1)
    # STRG + C will kill also
    except KeyboardInterrupt:
        run_event.clear()
        for proc in threads:
            threads[proc].join()


if __name__ == '__main__':
    main()
