#!/usr/bin/env python

import cv2
import numpy as np
import LaserTracking

BAD_COUNT_INIT = 5
GOOD_COUNT_GOAL = 2

class MinMaxPointStruct():
    def __init__(self, minPoint, maxPoint):
        self.min = minPoint
        self.max = maxPoint

class PointStruct():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TyPositionGoal():
    def __init__(self, videoChannel, debugging = 0):
        self.cam = cv2.VideoCapture(videoChannel)
        self.laserTracking = LaserTracking.LaserTracking(debugging)

        self.robotLimits = MinMaxPointStruct(minPoint = PointStruct(-120, -15), 
                                            maxPoint = PointStruct(120,105))
        self.cameraLimits = MinMaxPointStruct(minPoint = PointStruct(0, 0), 
                                            maxPoint = PointStruct(640,420))
        self.clickEvent = False
        self.clickPoint = PointStruct(0,0)
        self.cameraImageName = 'Ty View'
        self.badCount = 0
        self.goodCount = 0
        self.goalPoint = PointStruct(0,0)

    def mouseClick(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.clickEvent = True
            self.clickPoint.x = x
            self.clickPoint.y = y

    def startCalibration(self):
        # swap the current limits so the new ones can go in with simple comparisons to existing limits
        tmp = self.robotLimits.max
        self.robotLimits.max = self.robotLimits.min
        self.robotLimits.min = tmp

        tmp = self.cameraLimits.max
        self.cameraLimits.max = self.cameraLimits.min
        self.cameraLimits.min = tmp
        
    def getCalibrationPoint(self, robotx, roboty):
        self.clickEvent = False
        ret, frame = self.cam.read()
        cv2.imshow(self.cameraImageName, frame)
        self.img = frame
        resp = cv2.waitKey(20) & 0xFF

        cv2.setMouseCallback(self.cameraImageName, self.mouseClick)
        while self.clickEvent == False and resp != ord('q'):
            ret, frame = self.cam.read()
            cv2.imshow(self.cameraImageName, frame)
            self.img = frame
            resp = cv2.waitKey(20) & 0xFF
        if self.clickEvent == True:
            self.checkAgainstLimits(PointStruct(robotx, roboty), self.robotLimits)
            self.checkAgainstLimits(self.clickPoint, self.cameraLimits)
            self.printLimits('robot', self.robotLimits)
            self.printLimits('camera', self.cameraLimits)
            return True
        return False # out of range

    def printLimits(self, s, limits):
        print '%s min %s, max %s'% (s, [limits.min.x, limits.min.y], [limits.max.x, limits.max.y])

    def checkAgainstLimits(self, point, limits):
        if point.x > limits.max.x: limits.max.x = point.x
        if point.x < limits.min.x: limits.min.x = point.x
        if point.y > limits.max.y: limits.max.y = point.y
        if point.y < limits.min.y: limits.min.y = point.y


    def tf_stretch(self, a, b, aval):
        atotalx = a.max.x - a.min.x
        btotalx = b.max.x - b.min.x
        factor = (aval.x - a.min.x) / float(atotalx)
        bvalx =  (factor * btotalx) + b.min.x

        atotaly = (a.max.y - a.min.y)
        btotaly = -(b.max.y - b.min.y)
        factor = (aval.y - a.min.y) / float(atotaly)
        bvaly =  (factor * btotaly) + b.max.y

        return int(bvalx), int(bvaly)

    def tf_cam_to_robot(self, camx, camy):
        outx, outy = self.tf_stretch(self.cameraLimits, self.robotLimits, PointStruct(camx,camy))
        return (outx, outy)


    def getPositionGoalForThisFrame(self):
        ret, frame = self.cam.read()
        cv2.imshow(self.cameraImageName, frame)
        self.img = frame
        cv2.waitKey(1)

        if True == ret:
            p = self.laserTracking.getLaserPosition(frame)
            if p:
                return p
        return None # still here? that's bad

    def getPositionGoal(self):
        p = self.getPositionGoalForThisFrame()                
        if p == None:
            if self.badCount == 0 :          
                self.goodCount = 0
                return None
            else : # might be a blip, use last goal point
                self.badCount -= 1
                return (self.tf_cam_to_robot(self.goalPoint.x, self.goalPoint.y))        
        else: # got a good result ... but is it real?
            self.goodCount += 1
            if self.goodCount > GOOD_COUNT_GOAL:
                self.badCount = BAD_COUNT_INIT
                self.goalPoint.x = p[0]
                self.goalPoint.y = p[1]
                return(self.tf_cam_to_robot(self.goalPoint.x, self.goalPoint.y))
            else:
                return None

    def killWindows(self):
        cv2.destroyAllWindows()

            
    def __del__(self):
        self.cam.release()
        cv2.destroyAllWindows()


