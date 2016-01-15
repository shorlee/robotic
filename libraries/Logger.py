__author__ = 'Timo Boldt'

import sys
import logging


class Logger:

    def __init__(self, log_facility="info", log_file="/dev/null", log_print=True, log_syslog=False, app="ctrl"):
        # loglevels we support
        self.LOG_FACILITIES = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL}

        self.app_name = app
        self.logger = logging.getLogger(self.app_name)

        # check for configured logging level, if set use it, otherwise set to INFO
        if log_facility in self.LOG_FACILITIES:
            self.__log_level = self.LOG_FACILITIES[log_facility]
        else:
            self.__log_level = logging.INFO

        # check if log should be print to stdout
        if log_print:
            self.log_print = bool(log_print)
            if self.log_print:
                ch = logging.StreamHandler()
                self.logger.addHandler(ch)
                self.logger.setLevel(self.LOG_FACILITIES[log_facility])

        # open log file, if needed and append lines
        if log_file and log_file != 'None':
            fh = logging.FileHandler(log_file)
            self.logger.addHandler(fh)

    # log messages by logger
    def log(self, message="", log_facility="info", log_name=""):
        func = getattr(self.logger, log_facility)
        func(message)

    # quit the programm after logging
    def log_quit(self, message="", log_level=logging.CRITICAL, rc=1):
        self.log(message, log_level)
        sys.exit(int(rc))

    def set_debug(self, enabled=False):
        if enabled:
            self.logger.setLevel(self.LOG_FACILITIES["debug"])
        else:
            self.logger.setLevel(self.__log_level)

