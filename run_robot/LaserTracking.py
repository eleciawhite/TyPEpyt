#!/usr/bin/env python

import cv2
import numpy as np

class LaserTracking():
    def __init__(self, debugging = 0):
        self.debugging = debugging

    def getLaserPosition(self, frame):
        self.debugShow('cam', frame)
        laser_mask = self.maskLaser(frame)
        arm_mask = self.maskArm(frame)

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.debugShow('combo arm and laser', cv2.merge((gray_frame, arm_mask, laser_mask)))
        cv2.waitKey(1)

        laserDotContour = self.findContourOfLaserPointerDot(laser_mask)
        if laserDotContour != None:
            return self.getLaserCentroid(laserDotContour)
        else:
            return None       

    def findContourOfLaserPointerDot(self, laser_mask):
        (image, contours, heirarchy) = cv2.findContours(laser_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            print "x %d y %d r %d"%(x,y,radius)
            if radius > 7: 
                return c
            else:
                # anything else is too small
                return None
            
   # internal functions
    def mask(self, img, upper_in, lower_in):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array(lower_in)
        upper = np.array(upper_in)
        mask = cv2.inRange(hsv, lower, upper)
        return mask

    def maskLaser(self, img):
        # The red hue is split so it is 0 to 10 and 170 to 180
        m_hi = self.mask(img, [180, 50, 255], [170, 0,253])                    
        m_lo = self.mask(img, [10, 50, 255], [0, 0,253])   
        m1 = cv2.bitwise_or(m_hi, m_lo)
        
        # The result is a bit noisy, catching stray red speckles
        kernel = np.ones((3,3), np.uint8)
        m2 = cv2.dilate(m1, kernel, iterations = 3) # pump up the pixels until the laser ones touch
        m3 = cv2.erode(m2, kernel, iterations = 4)  # take away everything that isn't big enough
        m4 = cv2.dilate(m3, kernel, iterations = 3) # pump up the remaining
        m5 = cv2.erode(m4, kernel, iterations = 2)  # take away anything that is too small
        m6 = cv2.dilate(m5, kernel, iterations = 3) # pump up what is hopefully the laser

        return m6

    def getLaserCentroid(self, mask): # from mask
        M = cv2.moments(mask)
        if M['m00'] > 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            return (cx, cy)
        return None

    def maskArm(self, img):
        m1 =  self.mask(img, [40, 220, 255], [0, 90, 100])
        kernel = np.ones((3,3), np.uint8)
        m = cv2.dilate(m1, kernel, iterations = 1)
        return m 

    def debugPrint(self, s):
        if (self.debugging):
            print s

    def debugShow(self, s, img):
        if (self.debugging):
            cv2.imshow(s, img)


