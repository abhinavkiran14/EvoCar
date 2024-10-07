import logging
import time

import cv2
import numpy as np
import matplotlib.pyplot as plt

from line import Line, Quad

"""
expects an image in HSV format!
returns the image but with a blue mask applied
"""

def apply_blue_mask(img):
    lower_blue = np.array([90, 90, 50], dtype = "uint8")
    upper_blue = np.array([130, 255, 255], dtype = "uint8")
    return cv2.inRange(img, lower_blue, upper_blue)

def apply_red_mask(img):
    # the left side of the hue
    lower_red = np.array([0, 20, 50], dtype = "uint8")
    upper_red = np.array([30, 255, 255], dtype = "uint8")

    # the right side of the hue
    lower_red1 = np.array([160, 20, 50], dtype = "uint8")
    upper_red1 = np.array([179, 255, 255], dtype = "uint8")

    mask_red = cv2.inRange(img, lower_red, upper_red)
    mask_red1 = cv2.inRange(img, lower_red1, upper_red1)
    return cv2.bitwise_or(mask_red, mask_red1)

# expects a mask
# returns an an array of midlines for each contour eg each color
def find_lines(mask) -> [[Line]]:
    # generate contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    midlines = []
    for c in contours:
        area = cv2.contourArea(c) # Area of countour

        # remove too small areas
        if area < 1000:
            continue

        points = cv2.approxPolyDP(c, 0.009 * cv2.arcLength(c, True), False) # vertices of this contour object
        points = np.squeeze(points) # remove unnecessary insetness

        # the minimum length of line
        MINLEN = 10000

       # generate lines from the points
        lines = [ Line(points[i], points[(i+1) % len(points)]) for i in range(len(points))]
        lines.sort(reverse = True)


        # remove all lines that are too short
        for i in range(len(lines)):
            if lines[i].l < MINLEN:
                lines = lines[:i]
                break

        cmidlines = []

        # finds all midlines of a contour
        while len(lines) != 0:
            angle = lines[0].ang # angle of longest line

            # ln = all lines within ten degrees of longest
            ln = [l for l in lines if abs(angle - l.ang) < 10]
            # remove the longest line itself
            ln = ln[1:]

            if len(ln) == 0:
                # if a line has no partner we use the line itself
                cmidlines.append(lines[0])
                lines.remove(lines[0])
            else:
                # if there is another line we find its quad
                q1 = Quad(lines[0], ln[0])
                cmidlines.append(q1.mid)
                # remove used lines
                lines.remove(lines[0])
                lines.remove(ln[0])

            midlines += cmidlines

    return midlines

def find_true_line(midlines:[Line]) -> Line:
    assert(len(midlines) != 0)

    lowest = midlines[0]
    lowest_height:int = lowest.get_lowest_pos()
    for line in midlines[1:]:
        if line.get_lowest_pos() > lowest_height: # this could be wrong
            lowest = line
            lowest_height = line.get_lowest_pos()

    return lowest

def find_mid_line(l1:Line, l2:Line) -> Line:
    return Quad(l1, l2).mid

"""
0 = all good used both lines
1 = no lines all bad
2 = only saw red
3 = only saw blue
"""
def process(image):
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    blue_mask = apply_blue_mask(img_hsv)
    red_mask = apply_red_mask(img_hsv)

    arr_blue = find_lines(blue_mask)
    arr_red = find_lines(red_mask)

#    cv2.imshow("", apply_red_mask(img_hsv))
#    cv2.imshow("", blue_mask)

    if bool(arr_blue) and bool(arr_red):
        bluelow = find_true_line(arr_blue)
        redlow = find_true_line(arr_red)
        return find_mid_line(bluelow, redlow), 0

    elif arr_red:
        return find_true_line(arr_red), 2
    elif arr_blue:
        return find_true_line(arr_blue), 3
    else:
        return None, 1
