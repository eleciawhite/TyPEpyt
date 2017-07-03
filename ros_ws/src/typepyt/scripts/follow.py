#!/usr/bin/env python

import cv2
import numpy as np

VIDEO_CHANNEL = 1

cap = cv2.VideoCapture(VIDEO_CHANNEL)

def mask(img, upper, lower):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(hsv, lower_red, upper_red)
    upper_red = np.array([190, 255, 255])
    lower_red = np.array([170, 50, 50])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    mask = mask0+mask1
    return mask


def mask(img, upper_in, lower_in):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array(lower_in)
    upper = np.array(upper_in)
    mask = cv2.inRange(hsv, lower, upper)
    return mask

def mask_laser(img):
    return mask(img, [90, 10, 255], [40, 0,253])

def mask_arm(img):
    return mask(img, [40, 220, 255], [0, 90, 150])

def show_img(img):
    while cv2.waitKey(10) != ord('q'):
        cv2.imshow('show', img)
    cv2.destroyAllWindows()


while cv2.waitKey(10) != ord('q'):
    ret, frame = cap.read()
    cv2.imshow('laser', mask_laser(frame))


while cv2.waitKey(10) != ord('q'):
    ret, frame = cap.read()
    cv2.imshow('laser', mask_arm(frame))


while cv2.waitKey(10) != ord('q'):
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow('mask', hsv)


cap.release()
cv2.destroyAllWindows()

while cv2.waitKey(10) != ord('q'):
    cv2.imshow('frame',mask(frame))

