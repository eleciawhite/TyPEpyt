import numpy as np
import cv2
from matplotlib import pyplot as plt
import math


def getCam():
    videoChannel = 1
    cam = cv2.VideoCapture(videoChannel)
    return cam

def takePic():
    resp = 0
    while (resp  != ord('q')):
        ret, frame = cam.read()
        cv2.imshow("a", frame)
        resp = cv2.waitKey(20) & 0xFF
    cv2.destroyAllWindows()
    return frame

def keyboardLocation(keyboardImage, currentImage):
    kp_keys, kp_current, matches = getFlannInfo(keyboardImage, currentImage)
    goodMatches = getFlannMatchThresh(matches,threshold = 0.6)
    info = flannInfo(kp_keys, kp_current, goodMatches)
    print "distance: ", medianAt(3,info)
    print "angle: ", medianAt(4,info)


def getFlannInfo(queryImage, trainingImage):
    # create SIFT and detect/compute
    sift = cv2.xfeatures2d.SIFT_create()    
    kp1, des1 = sift.detectAndCompute(queryImage,None)
    kp2, des2 = sift.detectAndCompute(trainingImage,None)

    # FLANN matcher parameters
    # FLANN_INDEX_KDTREE = 0
    indexParams = dict(algorithm = 0, trees = 5)
    searchParams = dict(checks=50)   # or pass empty dictionary

    flann = cv2.FlannBasedMatcher(indexParams,searchParams)

    matches = flann.knnMatch(des1,des2,k=2)
    return kp1, kp2, matches

def getFlannMatchThresh(matches, threshold=0.7):
    good = []

    for m,n in matches:
        if m.distance < threshold*n.distance:
            good.append([m])
    return good

def distance(a, b):
    d = (a[0]-b[0])**2 + (a[1]-b[1])**2 
    return math.sqrt(d)

def angle(a,b):
    v = a[0] - b[0]
    h = a[1] - b[1]
    return (math.atan2(v,h))*180.0/math.pi

def medianAt(idx, inputlist):
    middle = int(len(inputlist)/2)
    return (sorted(inputlist, key=lambda s: s[idx]))[middle]


def flannInfo(kp_query, kp_train, matches):
    i =0
    out = []
    for mn in matches:
        m = mn[0]
        q = kp_query[m.queryIdx]
        t = kp_train[m.trainIdx]
        xoff = q.pt[0] - t.pt[0]
        yoff = q.pt[1] - t.pt[1]
        out.append((m.distance,  xoff, yoff, distance(q.pt, t.pt), angle(q.pt, t.pt))) 
    return out       


def showFlann(queryImage, trainingImage, threshold=0.7):
    kp1, kp2, matches = getFlannInfo(queryImage, trainingImage)
    goodMatches = getFlannMatchThresh(matches,threshold)

    resultImage = cv2.drawMatchesKnn(queryImage,kp1,
                                    trainingImage,kp2,
                                    goodMatches,trainingImage, flags=2)

    plt.imshow(resultImage,)
    plt.show()


def showFlannH(img1, img2):
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
        if m.distance < 0.7*n.distance:
            good.append(m)

    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)

        img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

    else:
        print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
        matchesMask = None

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)

    img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)

    plt.imshow(img3, 'gray'),plt.show()



def showCorners(origImg, sobel=23, thresh=0.01):
    img = cv2.cvtColor(origImg.copy(), cv2.COLOR_RGB2BGR) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 9, 23, 0.04)
    img[dst>thresh * dst.max()] = [255, 0, 0] 

    plt.imshow(img,)
    plt.show()

