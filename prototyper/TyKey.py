import numpy as np
import cv2
from matplotlib import pyplot as plt
import math
import keyboardCalibration as KeyCal

class KeyMap():
    def __init__(self, cam, debugging = 0):
        self.cam = cam
        self.debugging = debugging
        self.keyImg = cv2.imread("keys.png")
        self.cameraImageName = 'Ty View'
        self.clickEvent = False
        self.outline = None
        self.cannyThresh = 1000

    def mouseClickCallback(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.clickEvent = True
            self.clickPoint = [x, y]

    def transformKeyboardToCameraPos(self, c):
        pos = KeyCal.KEYPIX[c]
        a = np.array([[pos]], dtype='float32')
        return cv2.perspectiveTransform(a,self.M)[0][0]

    def transformCameraPosToKeyboard(self, t):
        a = np.array([[t]], dtype='float32')
        return cv2.perspectiveTransform(a,self.Minv)[0][0]
       
    def keyPosToChar(self, found):
        foundChar = []
        for c in KeyCal.KEYPIX:
            chx = KeyCal.KEYPIX[c][0]
            chy = KeyCal.KEYPIX[c][1]
            if abs(chx-found[0]) < 20 and abs(chy-found[1]) < 15:
                foundChar.append(c)
        return foundChar

    def charToKeyPos(self, c):
        return KeyCal.KEYPIX[c]

    def waitForClick(self):
        self.clickEvent = False
        ret, frame = self.cam.read()
        cv2.imshow(self.cameraImageName, frame)
        resp = cv2.waitKey(20) & 0xFF
        cv2.setMouseCallback(self.cameraImageName, self.mouseClickCallback)

        while self.clickEvent == False and resp != ord('q'):
            ret, frame = self.cam.read()
            cv2.imshow(self.cameraImageName, frame)
            self.img = frame.copy()
            resp = cv2.waitKey(20) & 0xFF
        cv2.destroyAllWindows()
        return frame


    def kvm(self, debugDraw = False):
        frame = self.waitForClick()

        if self.clickEvent == True:
            frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
            self.M, outline = self.getHoloM(self.keyImg, frame, debugDraw=debugDraw)
            if (self.M is not None):
                self.outline = outline
                self.Minv = np.linalg.inv(self.M)
                out = self.transformCameraPosToKeyboard(self.clickPoint)
                print "Point ", out, " is key: ", self.keyPosToChar(out)
                claw_location = self.locateClaw(self.img, outline)
                if (claw_location is not None):
                    claw_xform = self.transformCameraPosToKeyboard(claw_location)
                    print "Claw ", claw_xform, " is key: ", self.keyPosToChar(claw_xform)
        
        return self.img, outline

    def locateClaw(self, frame = None, outline = None, debugDraw=False):
        if (frame is None):
            print "Frame not passed in."
            ret, frame = self.cam.read()
            self.img = frame
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        # define range of blue color in HSV
        lower_blue = np.array([5,150,180])
        upper_blue = np.array([20,195,255])

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        e = cv2.dilate(mask, np.ones((3,3),np.uint8), iterations=2)
        circles = cv2.HoughCircles(e,cv2.HOUGH_GRADIENT, 1, 100, 
                    param1=self.cannyThresh, param2=1, minRadius=0,maxRadius=10)
        if debugDraw is True:
            plt.subplot(221)
            plt.imshow(cv2.Canny(mask, self.cannyThresh, self.cannyThresh/2), cmap = "gray"), plt.title("Canny Mask")
            plt.subplot(222)
            plt.imshow(e, cmap = "gray"), plt.title("Dilated")
            plt.subplot(223)
            plt.imshow(cv2.Canny(e, self.cannyThresh, self.cannyThresh/2), cmap = "gray"), plt.title("Canny Dilated")
            plt.subplot(224)

        if (circles is None):
            print "Error: Could not locate claw!"
            return None

        circles = circles[0,:]
        goodCircles = self.findGoodCircles(circles, outline)
        fc = self.drawCircles(circles, frame, color = (0,0,255), show = False)
        self.drawCircles(goodCircles, fc, color = (0, 255,0), show = debugDraw)
        if len(goodCircles) == 0:
            claw = None
        else:
            claw = (goodCircles[0][0], goodCircles[0][1]) # most accumulation            
        return claw

    def findGoodCircles(self, circles, outline):
        if (outline is None):
            outline = self.outline
        if (outline is None):
            print "ERROR!! Run kvm before locate Claw to create keyboard outline!"
        circles = np.uint16(np.around(circles))
        goodCircles = []
        for i in circles:
            if (outline is not None) and (cv2.pointPolygonTest(outline, (i[0],i[1]), False) > 0.0):
                goodCircles.append(i)
        print "There are ", len(circles), " originally, ", len(goodCircles), " good ones: ", goodCircles
        return goodCircles

    def drawCircles(self, circles, frame, outline=None, color=(0,255, 255), show = True):            
        fc = cv2.cvtColor(frame.copy(), cv2.COLOR_RGB2BGR)
        for i in circles:
            cv2.circle(fc,(i[0],i[1]),i[2],color,2)
        if show is True:
            plt.imshow(fc),plt.show()
        return cv2.cvtColor(fc, cv2.COLOR_BGR2RGB)

    def getHoloM(self, img1, img2, threshold=0.7, debugDraw=True):
        MIN_MATCH_COUNT = 10
        # Initiate SIFT detector
        sift = cv2.xfeatures2d.SIFT_create()

        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img1,None)
        kp2, des2 = sift.detectAndCompute(img2,None)


        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(des1,des2,k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m,n in matches:
            if m.distance < threshold*n.distance:
                good.append(m)

        if len(good) >= MIN_MATCH_COUNT:
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
            matchesMask = mask.ravel().tolist()

            h,w = img1.shape[0:2]
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            outline = cv2.perspectiveTransform(pts,M)

            img2 = cv2.polylines(img2,[np.int32(outline)],True,255,3, cv2.LINE_AA)

        else:
            print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
            matchesMask = None
            M = None

        if debugDraw == True:
            draw_params = dict(
                           singlePointColor = None,
                           matchesMask = matchesMask, # draw only inliers
                           flags = 2)

            img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)

            plt.imshow(img3, 'gray'),plt.show()
        return M, outline




if __name__ == '__main__':
    try: cam
    except NameError: 
        videoChannel = 1
        cam = cv2.VideoCapture(videoChannel)
    k = KeyMap(cam)
    k.kvm()


