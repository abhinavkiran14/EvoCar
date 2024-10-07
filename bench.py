#!/usr/bin/env python3

import time

import cv2

import img_proc
from evocar import Evocar
from load_settings import Settings
from videoget import VideoGet

if __name__ == "__main__":
    settings = Settings()

    test_car = Evocar(settings.ip, settings.port, settings.camport)
    test_car.setcamera(True)

    then = time.time()
    img_proc.process(cv2.imread("images/new_car1.jpg"))
    now = time.time()
    print("time to proc: %.4f" % (now - then))

    then = time.time()
    test_car.make_wheel_request(0, 0) # we should set a timeout on wheel requests
    now = time.time()
    print("time to send cmd: %.4f" % (now - then))

    vg = VideoGet(test_car)
    t = vg.start()
    time.sleep(2)
    then = time.time()
    vg.get_frame()
    now = time.time()
    print("time to fetch frame(not http): %.4f" % (now - then))

    # this exists so that the framerate logged by vg.stop() is more accurate as it has more data points.
    # Additionally data collection appears to accelerate over time in the beginning.
    time.sleep(1) 
    vg.stop()
