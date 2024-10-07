#!/usr/bin/env python3
import enum
import json
import os
import time
import http
import urllib
import urllib.request
import unittest

class Evocar:
    def __init__(self, ip:str, port:int, camport:int):
        self.ip = ip;
        self.port = port;
        self.camport = camport;
        self.pos:dict[str, int] = {}

    # encodes a dictionary to be sent over network in a get request
    def encode_dict(d) -> str:
        res: str = ""
        for k, v in d.items():
            res += k + "%3A" + str(v) + "%2C"
        res = res[:-3]
        return res

    def request_prefix(self):
        return "http://%s:%d/command?cmd=direct&v1=" % (self.ip, self.port)

    def make_generic_request(self, data):
        self.pos.update(data) # update current positions
        s:str = self.request_prefix() + Evocar.encode_dict(data)
        return urllib.request.urlopen(s)

    def make_wheel_request(self, left:int, right:int, switch_lr = False):
        # this is in wheel_request because arm motions can be precise
        matches = True


        if switch_lr:
            d = {"L":right, "R":left}
        else:
            d = {"L":left, "R":right}

        for k, v in d.items():
            # if the difference from the last command in one param is greater than 5 listen
            if (k not in self.pos) or abs(self.pos[k] - d[k]) > 0:
                matches = False
                break

        if matches:
            return None
        return self.make_generic_request( d )

    def stop(self):
        return self.make_wheel_request(0, 0)

    def setcamera(self, on: bool):
        return urllib.request.urlopen("http://%s:%d/command?cmd=service%s&v1=camera" % (self.ip, self.port, ("start" if on else "stop")))

    def restartcamera(self):
        return urllib.request.urlopen("http://%s:%d/command?cmd=servicerestart&v1=camera" % (self.ip, self.port))

    def shutdown(self):
        return urllib.request.urlopen("http://%s:%d/command?cmd=shutdown" % (self.ip, self.port))

    def reboot(self):
        return urllib.request.urlopen("http://%s:%d/command?cmd=reboot" % (self.ip, self.port))

    def getpos(self) -> dict:
        s = json.loads(urllib.request.urlopen("http://%s:%d/getpos" % (self.ip, self.port)).read().decode("utf-8"))
        splitup = [i.split(":") for i in s["pos"].split(",")]
        return {i[0]:int(i[1]) for i in splitup}

#    def camconfig(self, framerate:int, resolution:str):
#        urllib.request.urlopen("http://%s:%d/camconfig?name=framerate&value=%d&type=int" % (self.ip, self.port, framerate))
#        urllib.request.urlopen("http://%s:%d/camconfig?name=resolution&value=%s&type=string" % (self.ip, self.port, resolution))

class TestEvocar(unittest.TestCase):
    def test_encode_dict(self):
        string = Evocar.encode_dict({"L":0, "R":0})
        self.assertEqual(string, "L%3A0%2CR%3A0")
