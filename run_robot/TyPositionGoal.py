#!/usr/bin/env python

import cv2
import numpy as np

VIDEO_CHANNEL = 1

class TyPositionGoal():
    def __init__(self, debugging = 0):
        self.cam = cv2.VideoCapture(VIDEO_CHANNEL)
        self.debugging = debugging

    def getPositionGoal(self):
        ret, frame = self.cam.read()
        if True == ret:
            self.debugShow('cam', frame)
            m = self.maskLaser(frame)
            return self.getLaserCentroid(m)
        return (-1, -2)
            
    def __del__(self):
        self.cam.release()
        cv2.destroyAllWindows()

   # internal functions
    def mask(self, img, upper_in, lower_in):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array(lower_in)
        upper = np.array(upper_in)
        mask = cv2.inRange(hsv, lower, upper)
        return mask

    def maskLaser(self, img):
        m = self.mask(img, [50, 50, 255], [0, 0,253])            
        self.debugShow('maskLaser', m)
        return m

    def getLaserCentroid(self, mask): # from mask
        M = cv2.moments(mask)
        if M['m00'] > 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            self.debugPrint('(x = %d, y = %d)'%(cx,cy))
            return (cx, cy)
        return (-1, -1)

    def mask_arm(self, img):
        m =  self.mask(img, [40, 220, 255], [0, 90, 150])
        self.debugShow('masArm', m)
        return m 

    #debugging
    def show_img(self, img):
        while cv2.waitKey(10) != ord('q'):
            cv2.imshow('show', img)
        cv2.destroyAllWindows()

    def debugPrint(self, s):
        if (self.debugging):
            print s

    def debugShow(self, s, img):
        if (self.debugging):
            cv2.imshow(s, img)
            cv2.waitKey(1)


#while cv2.waitKey(10) != ord('q'):
#    ret, frame = cam.read()
#    cv2.imshow('laser', frame)

