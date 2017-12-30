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

    def mouseClickCallback(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.clickEvent = True
            self.click_x = x
            self.click_y = y

    def transformQtoT(self, M, q):
        a = np.array([[q]], dtype='float32')
        return cv2.perspectiveTransform(a,M)

    def transformTtoQ(self, M, t):
        a = np.array([[t]], dtype='float32')
        return cv2.perspectiveTransform(a,np.linalg.inv(M))[0][0]
        
    def pixToChar(self, found):
        foundChar = []
        for c in KeyCal.KEYPIX:
            chx = KeyCal.KEYPIX[c][0]
            chy = KeyCal.KEYPIX[c][1]
            if abs(chx-found[0]) < 20 and abs(chy-found[1]) < 15:
                foundChar.append(c)
        return foundChar

    def kvm(self, debugDraw = False):
        self.clickEvent = False
        ret, frame = self.cam.read()
        cv2.imshow(self.cameraImageName, frame)
        resp = cv2.waitKey(20) & 0xFF
        cv2.setMouseCallback(self.cameraImageName, self.mouseClickCallback)

        while self.clickEvent == False and resp != ord('q'):
            ret, frame = self.cam.read()
            cv2.imshow(self.cameraImageName, frame)
            self.img = frame.copy()
            frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
            resp = cv2.waitKey(20) & 0xFF
        cv2.destroyAllWindows()
        if self.clickEvent == True:
            self.M, outline = self.getHoloM(self.keyImg, frame, debugDraw=debugDraw)
            if (self.M is not None):
                out = self.transformTtoQ(self.M, (self.click_x,self.click_y))
                print "Point ", out, " is key: ", self.pixToChar(out)
                claw_location = self.locateClaw(self.img, outline)
                if (claw_location is not None):
                    claw_xform = self.transformTtoQ(self.M, claw_location)
                    print "Claw ", claw_xform, " is key: ", self.pixToChar(claw_xform)
        
        return self.img, outline

    def locateClaw(self, frame, outline):
        yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        circles = cv2.HoughCircles(yuv[:,:,2],cv2.HOUGH_GRADIENT,4,200, param1=100, param2=40, minRadius=0,maxRadius=20)
#cv2.HoughCircles(yuv[:,:,2],cv2.HOUGH_GRADIENT,1,20, param1=100, param2=20, minRadius=0,maxRadius=20)
#cv2.HoughCircles(yuv[:,:,0],cv2.HOUGH_GRADIENT,1,20,param1=50, param2=35, minRadius=0,maxRadius=20)
#cv2.HoughCircles(yuv[:,:,2],cv2.HOUGH_GRADIENT,4,200, param1=100, param2=60, minRadius=0,maxRadius=20)
#cv2.HoughCircles(yuv[:,:,0],cv2.HOUGH_GRADIENT,1,20,param1=100, param2=30, minRadius=0,maxRadius=100)

        if (circles is None):
            print "Error: Could not locate claw!"
            return None
        #else 
        circles = np.uint16(np.around(circles))
        goodCircles = []
        fc = cv2.cvtColor(frame.copy(), cv2.COLOR_RGB2BGR)
        for i in circles[0,:]:
            # draw the outer circle
            if cv2.pointPolygonTest(outline, (i[0],i[1]), False) > 0.0:
                cv2.circle(fc,(i[0],i[1]),i[2],(0,255,0),2)
                goodCircles.append(i)
            else:
                cv2.circle(fc,(i[0],i[1]),i[2],(255,0,0),2)

        print "There are ", (len(circles[0])), " originally, ", len(goodCircles), " good ones."
        plt.imshow(fc),plt.show()
        if len(goodCircles) == 0:
            claw = None
        else:
            claw = (goodCircles[0][0], goodCircles[0][1]) # most accumulation            
        return claw

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





# USAGE
# execfile('TyKey.py')
#videoChannel = 1
#cam = cv2.VideoCapture(videoChannel)
#k = KeyMap(cam)
#k.kvm()



