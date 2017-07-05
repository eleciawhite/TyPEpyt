#!/usr/bin/env python

import cv2
import numpy as np
import LaserTracking

VIDEO_CHANNEL = 2 # 'ls /dev/video*' and choose the channel right for you

class TyPositionGoal():
    def __init__(self, debugging = 0):
        self.cam = cv2.VideoCapture(VIDEO_CHANNEL)
        self.laserTracking = LaserTracking.LaserTracking(debugging)

    def getPositionGoal(self):
        ret, frame = self.cam.read()
        if True == ret:
            return self.laserTracking.getLaserPosition(frame)
        else: 
           return None
            
    def __del__(self):
        self.cam.release()
        cv2.destroyAllWindows()


