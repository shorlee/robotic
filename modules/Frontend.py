__author__ = 'Andrej Frank'
__version__ = '1.0.0'

import sys
from PyQt5 import QtWidgets, uic
from threading import Thread
from time import sleep
import libraries.icon_rc as icon_rc


class Frontend(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        # PyQt Designer Layout laden
        self.__ui = uic.loadUi("config/Controller.ui", self)

        #X-Slider verbinden und min. & max. des Sliders setzen
        self.__ui.xSlider.valueChanged[int].connect(self.set_slider_x)
        self.__ui.xSlider.setMinimum(-100)
        self.__ui.xSlider.setMaximum(100)

        #Y-Slider verbinden und min. & max. des Sliders setzen
        self.__ui.ySlider.valueChanged[int].connect(self.set_slider_y)
        self.__ui.ySlider.setMinimum(-100)
        self.__ui.ySlider.setMaximum(100)

        # speed slider
        self.__ui.speed.valueChanged[int].connect(self.set_speed_bar)
        self.__ui.speed.setMinimum(0)
        self.__ui.speed.setMaximum(100)

        # GUI anzeigen lassen
        self.show()

    # X-Slider setzen, für Joypad
    def set_slider_x(self, value):
        self.__ui.xSlider.setValue(value)

    def set_slider_y(self, value):
        self.__ui.ySlider.setValue(value)

    def set_speed_bar(self, value):
        self.__ui.speed.setValue(value)

    def set_direction(self, value):
        self.__ui.directionDial.setValue(value)

    def set_connected(self, value):
        if value:
            self.__ui.controller_connected.setText("Controller connected")
            self.__ui.controller_connected.setStyleSheet("background-color : green")
        else:
            self.__ui.controller_connected.setText("Controller disconnected")
            self.__ui.controller_connected.setStyleSheet("background-color : red")

    def set_move_type(self, mtype):
        button = getattr(self.__ui, mtype)
        button.setChecked(True)


def value_setter(main_window, data, logger, config, app, run_event):
    """
    function to set frontend information
    :param mainWindow:
    :param data:
    """
    connected = False
    connected_old = False
    move_type = None
    while run_event.is_set():
        if "axis" in data and "x" in data["axis"] and "y" in data["axis"]:
            main_window.set_slider_x(data["axis"]["x"] * 100)
            main_window.set_slider_y(data["axis"]["y"] * 100)
            main_window.set_direction(data["axis"]["angle"] + 180)
            main_window.set_speed_bar(data["axis"]["speed"] * 100)

            # check if connection state changed
            connected = data["ctrl"]["connected"]
            if connected != connected_old:
                main_window.set_connected(data["ctrl"]["connected"])
            connected_old = data["ctrl"]["connected"]

            if move_type != data["ctrl"]["mode"]:
                move_type = data["ctrl"]["mode"]
                main_window.set_move_type(move_type)

            logger.log(data, "debug")
        sleep(0.1)

    app.closeAllWindows()
    app.quit()


# worker function that is called by master process
def worker(data, logger, config, run_event):

    # start QApplication with empty list as parameter (needs list!)
    app = QtWidgets.QApplication([])
    # spawn Frontend-object
    main_window = Frontend()

    # starting thread which will set values into the frontend
    t = Thread(target=value_setter, args=[main_window, data, logger, config, app, run_event])
    t.start()

    # start main frontend
    app.exec()
