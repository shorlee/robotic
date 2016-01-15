__author__ = 'David Ossenkopp'
__version__ = '1.0.0'

import pygame
import time
import math
import sys
import datetime

if sys.platform == 'linux':
    import usb


# check if value is between range, otherwise return 0! we need to compensate the offset of joystick
# Range is -1 -> -OFFSET || OFFSET -> 1  (e.g. -1 -> -0.15  || 0.15 -> 1)
def axis_in_range(value, offset=0.0):
    # positive offset till 1
    if 1 >= value >= offset:
        return value
    # -1 till negativ offset
    elif offset * (-1) >= value >= -1:
        return value
    return 0


class Controller:

    def __init__(self, logger, config):
        pygame.init()

        self.__config = config
        self.__config_controller = config.get_controller()

        self.clock = pygame.time.Clock()
        self.controller_init()

        self.__joystick = None
        self.__axis_x = 0
        self.__axis_y = 0
        self.__controller_connected = None
        self.__logger = logger
        self.__debug_mode = False
        self.__debug_button = False

        # debugging button delta time calculation
        self.__d1_set = False
        self.__d2_set = False
        self.__d1 = None
        self.__d2 = None

        # debugging button delta time calculation
        self.__t1_set = False
        self.__t2_set = False
        self.__t1 = None
        self.__t2 = None

    def controller_init(self):
        """
        initalize the controller and joysticks
        :return:
        """
        try:
            pygame.joystick.quit()
            pygame.joystick.init()
            joystick_count = pygame.joystick.get_count()

            if joystick_count == 0:
                pass

            for i in range(joystick_count):
                self.__joystick = pygame.joystick.Joystick(i)
                self.__joystick.init()
                if self.__joystick:
                    self.__controller_connected = True
                    return True

        except Exception as e:
            self.__logger.log(e, "debug")
            self.__controller_connected = False
            return False

    def get_axis_x(self):
        axis_id = int(self.__config_controller["axis_x"])
        axis_offset = float(self.__config_controller["axis_offset"])
        self.__axis_x = axis_in_range(self.__joystick.get_axis(axis_id), axis_offset)
        return self.__axis_x

    def get_axis_y(self):
        axis_id = int(self.__config_controller["axis_y"])
        axis_offset = float(self.__config_controller["axis_offset"])
        self.__axis_y = axis_in_range(self.__joystick.get_axis(axis_id) * (-1), axis_offset)
        return self.__axis_y

    def get_speed(self):
        axis_id = int(self.__config_controller["axis_speed"])
        if sys.platform == 'win32' or sys.platform == "win64":
            return 0 - self.__joystick.get_axis(axis_id)
        elif sys.platform == 'linux':
            return (1 + self.__joystick.get_axis(axis_id)) / 2

    def get_angle(self):
        """ caculate radiant in degree (forward is 0°)
        :return: float
        """
        angle = self.get_radiant() / (2 * math.pi) * 360

        if angle < 0:
            return 360 + angle
        elif angle == 0:
            return 0
        return angle

    def get_radiant(self):
        """
        returns radiant, 0 -> up, left -> PI/2, down -> PI, right -> 3/4 PI
        :return:
        """
        if self.__axis_x == 0 and self.__axis_y == 0:
            return 0
        raw = math.atan2(self.__axis_y, self.__axis_x) - (math.pi/2)
        if raw < 0:
            raw += (math.pi * 2)
        return raw

    def get_move_type(self):
        if self.__joystick.get_button(int(self.__config_controller["button_circle"])):
            return "circle"
        elif self.__joystick.get_button(int(self.__config_controller["button_triangle"])):
            return "triangle"
        elif self.__joystick.get_button(int(self.__config_controller["button_square"])):
            return "square"
        elif self.__joystick.get_button(int(self.__config_controller["button_cross"])):
            return "cross"

    def get_height_button(self):
        if self.__joystick.get_button(int(self.__config_controller["button_height"])):
            return True

        return False

    # check if debug should be enabled by select key
    def check_debug(self):
        if self.__joystick.get_button(int(self.__config_controller["button_debug"])) and not self.__d1_set:
            self.__d1_set = True
            self.__d1 = datetime.datetime.now()
        elif self.__d1_set and not self.__joystick.get_button(int(self.__config_controller["button_debug"])) and not self.__d2_set:
            self.__d2_set = True
            self.__d2 = datetime.datetime.now()

        if self.__d1_set and self.__d2_set:
            if 10 > (self.__d2 - self.__d1).seconds >= 0:
                if self.__debug_mode:
                    self.__logger.log("disable debug mode", "debug")
                    self.__debug_mode = False
                    self.__logger.set_debug(enabled=False)
                else:
                    self.__logger.log("enable debug mode", "info")
                    self.__debug_mode = True
                    self.__logger.set_debug(enabled=True)

            self.__d1_set = False
            self.__d2_set = False

        return self.__debug_mode

    def check_terminate(self):
        if self.__joystick.get_button(int(self.__config_controller["button_terminate"])) and not self.__t1_set:
            self.__t1_set = True
            self.__t1 = datetime.datetime.now()
        elif self.__t1_set and not self.__joystick.get_button(int(self.__config_controller["button_terminate"])) and not self.__t2_set:
            self.__t2_set = True
            self.__t2 = datetime.datetime.now()

        # kill if invertal between press and release of kill button is greater than 2
        if self.__t1_set and self.__t2_set:
            if 10 > (self.__t2 - self.__t1).seconds >= 2:
                self.__t1_set = False
                self.__t2_set = False
                return True
            else:
                self.__t1_set = False
                self.__t2_set = False
                return False


# check if gamepad is connected (depends on platform)
def check_connected(obj=None, vendor_id=0, product_id=0):
    if not obj:
        print("test")
        return False

    if sys.platform == 'win32' or sys.platform == 'win64':
        pygame.joystick.quit()
        return obj.controller_init()
    elif sys.platform == 'linux':
        try:
            found_device = False
            busses = usb.busses()
            for bus in busses:
                devices = bus.devices
                for dev in devices:
                    if int(dev.idVendor) == int(vendor_id) and int(dev.idProduct) == int(product_id):
                        found_device = True
            if not found_device:
                pygame.joystick.quit()

            return found_device

        except usb.core.USBError:
            return False
    else:
        pass


def worker(data, logger, config, run_event):
    try:
        obj = Controller(logger, config)

        con_connected = False
        while not con_connected:
            con_connected = obj.controller_init()
            time.sleep(0.01)

        data["axis"]["x"] = 0
        data["axis"]["y"] = 0
        speed_default = True

        vendor_id = config.get_controller()["vendor_id"]
        product_id = config.get_controller()["product_id"]

        counter = 0
        connected = None

        while run_event.is_set():
            obj.clock.tick(20)
            counter += 1

            if counter > 50:
                connected = check_connected(obj=obj, vendor_id=vendor_id, product_id=product_id)
                if not con_connected and connected:
                    obj.controller_init()
                counter = 0
                con_connected = connected

            data["ctrl"]["connected"] = con_connected

            for event in pygame.event.get():
                if not connected:
                    continue
                # check for terminate application
                if obj.check_terminate():
                    logger.log("controller terminate button pressed", "debug")
                    data["signal"]["terminate"] = True
                    return 0

                # check if debug key is pressed
                dbg = obj.check_debug()
                if dbg is not None:
                    data["ctrl"]["debug"] = dbg


                # check if height button is pressed
                height = obj.get_height_button()
                if height is not None:
                    data["ctrl"]["height"] = height

                # only set type if move_type changed
                move_type = obj.get_move_type()
                if move_type:
                    data["ctrl"]["mode"] = move_type

                data["axis"]["x"] = round(obj.get_axis_x(), 5)
                data["axis"]["y"] = round(obj.get_axis_y(), 5)
                data["axis"]["angle"] = round(obj.get_angle(), 5)
                data["axis"]["radiant"] = round(obj.get_radiant(), 5)
                data["ctrl"]["high"] = bool(obj.get_height_button())
                if speed_default:
                    if obj.get_speed() != 1.0:
                        speed_default = False
                else:
                    data["axis"]["speed"] = round(obj.get_speed(), 2)
                logger.log("X: %s   Y: %s   A: %s   R: %s   S: %s   T: %s   C: %s   H:%s" % (data["axis"]["x"], data["axis"]["y"],
                                                                                      data["axis"]["angle"],
                                                                                      data["axis"]["radiant"],
                                                                                      data["axis"]["speed"],
                                                                                      data["ctrl"]["mode"],
                                                                                      data["ctrl"]["connected"], data["ctrl"]["height"]), "debug")
                time.sleep(0.0001)
    except KeyboardInterrupt:
        return 0