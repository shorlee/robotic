import zmq
import json

class Zlib:
    def __init__(self, host, port):
        self.zHost = host
        self.zPort = port
        self.logger = None

        # maybe we want to use zmq context based socket? it supports send_string, send_json and such things ...
        self.context = zmq.Context()
        self.socket = None

    # defines, if object is server
    def server(self):
        self.socket = self.context.socket(zmq.PUB)
        self.logger.log("binding on %s:%s" % (self.zHost, self.zPort))
        self.socket.bind("tcp://%s:%s" % (self.zHost, int(self.zPort)))

    # defines, if object is client
    def client(self):
        self.socket = self.context.socket(zmq.SUB)
        topicfilter = "1"
        self.socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
        self.logger.log("connecting to %s:%s" % (self.zHost, self.zPort))
        self.socket.connect("tcp://%s:%s" % (self.zHost, int(self.zPort)))

    # set the logger class for further logging
    def set_logger(self, logger=None):
        self.logger = logger

    # returns a dict
    def recv(self):
        try:
            string = self.socket.recv_unicode()
            topic, messagedata = string.split(' ', 1)
            return json.loads(messagedata)
        except Exception as e:
            raise e

    # send message (dict)
    def send(self, message=dict()):
        try:
            msg = "%s %s" % (1, json.dumps(message))
            self.socket.send_unicode(msg)
        except Exception as e:
            raise e
