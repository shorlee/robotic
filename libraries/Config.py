import configparser
import os


class Config:

    def __init__(self, config_file):
        # defines the config files we load
        config_file = config_file
        config = configparser.ConfigParser()
        config.read(config_file)

        if not os.path.isfile(config_file):
            print("config file [%s] not found, loading default values!" % config_file)

        ################################
        # default configs
        ################################
        # defines the logger object
        self.conf = {
            "logging": {
                "log_level": "info",
                "log_file": "/dev/null",
                "log_print": True,
                "log_syslog": False
            },
            "network": {
                "host": "127.0.0.1",
                "port": 6666,
                "interval": 0.01
            },
            "controller": {
                "axis_speed": 5,
                "axis_x": 0,
                "axis_y": 1,
                "axis_offset": 0.15,
                "button_triangle": 99,
                "button_circle": 98,
                "button_square": 97,
                "button_cross": 96,
                "button_debug": 6,
                "button_terminate": 7,
            },
            "frontend": {
                "ui_file": "Controller.ui"
            }
        }

        # override default config parameters
        for section in config:
            for key in config[section]:
                self.conf[section][key] = config[section][key]

    def get_config(self):
        return self.conf

    def get_logging(self):
        return self.conf["logging"]

    def get_network(self):
        return self.conf["network"]

    def get_controller(self):
        return self.conf["controller"]

    def get_frontend(self):
        return self.conf["frontend"]


def get_bool(string):
    try:
        return string.lower() in ("yes", "true", "t", "1")
    except AttributeError:
        return False



