#!/usr/bin/env python3
import time
import signal
import sys

import cv2
import numpy as np

import evocar
from line import Line
from videoget import VideoGet
from load_settings import Settings
import img_proc


config = Settings()

MOTOR_MULT = 1
car = evocar.Evocar(config.ip, config.port, config.camport)
vg = VideoGet(car)


goal_ang = config.goal
err = 0
p_err = 0
sum_err = 0
diff_err = 0
run = True


def keyboardInterruptHandler(signal, frame):
    global car
    car.stop()
    print("STOP")
    vg.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)


def map_to_range(val, min1, max1, min2, max2):
    span1 = max1-min1
    span2 = max2-min2

    val_scaled = float(val - min1) / float(span1)
    out = float(min2 + (val_scaled * span2))

    if out > max2:
        return max2
    elif out < min2:
        return min2
    else:
        return out


def mainloop(frame, car):
    global sum_err, diff_err, p_err, config
    traj, status = img_proc.process(frame)

    # print(traj)
    # print(status)

    if status == 1:
        
        if p_err > 0:
            car.make_wheel_request(40, -40)
        elif p_err < 0:
            car.make_wheel_request(-40, 40)
        else:
            car.make_wheel_request(50, 50)
        
        return

    # make angle between 180 and 0
    angle = traj.ang % 180
    # calc error
    err = -(goal_ang - angle)

    print("err %.4f" % err)

    sum_err += err

    diff_err = err - p_err
    # use pid
    val = config.P*err + config.I*sum_err + config.D*diff_err
    offset = int(10 + (abs(goal_ang - angle)/7))

    # Turning starts at L:125 , R:15, if Speed = 70

    p_err = err

    if status == 0:
        pass # update previous error
    elif status == 2: # red was seen
        print("Only using Red")
        val /= 2
        if config.blue_on_right:
            val +=  offset
        else:
            val +=  -offset

    elif status == 3: # blue was seen
        print("Only using Blue")
        val /= 2
        if config.blue_on_right:
            val += -offset
        else:
            val += offset
    print(val)

#right min 14, -20
#left min 15, -15

    low_speed = -3
    high_speed = 17


    if val > 10:
        print("Turning Right")
        val = map_to_range(val, 10, 70, config.speed - high_speed, config.speed - low_speed)
    elif val < -10:
        print("Turning Left")
        val = map_to_range(val, -70, -10, -config.speed + low_speed, -config.speed + high_speed)
    else:
        val = 0

    ls = (config.speed + val) * MOTOR_MULT
    rs = (config.speed - val) * MOTOR_MULT

    car.make_wheel_request(ls, rs, switch_lr=config.switch_lr)

    print("val: %d" % val)
    print("Left: %d, Right: %d" % (ls, rs))

def main():
    global car, vg

    # TODO check if camera is on
    car.setcamera(True)
    time.sleep(2)
    vg.start()

    car.make_generic_request(config.arm_angles)

    while run:
        s = time.time()
        frame = vg.get_frame()
        if vg.grabbed != None:
            mainloop(frame, car)
#        print("seconds to send: %f" % (time.time() - s))
    car.stop()

if __name__ == "__main__":
    main()
