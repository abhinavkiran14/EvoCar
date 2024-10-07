from threading import Thread
import time

import cv2

import evocar


class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, car :evocar.Evocar):
        self.stream = cv2.VideoCapture("http://%s:%d/stream.mjpg" % (car.ip, car.camport))
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        self.timestamp = time.time()
        self.used_time = 0
        self.t = Thread(target=self.get, args=())
        self.start_time = time.time()
        self.frames = 0

    def start(self):
        self.t.start()

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.t.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()
                self.timestamp = time.time()
                self.frames += 1

    def get_frame(self):
        self.used_time = self.timestamp
        return self.frame if self.grabbed else None

    def stop(self):
        self.stopped = True
        print("fps: %.4f" % (self.frames/(time.time() - self.start_time)))
