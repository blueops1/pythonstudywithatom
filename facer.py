import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

while(1):

    #Take each frame
    _,frame = cap.read()

    #Convert BRG to HSV
    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)

    #define range of blue color in hsv
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    # threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv,lower_blue,upper_blue)

    #bitwise_and mask and original image
    res = cv.bitwise_and(frame,frame,mask=mask)

    cv.imshow('frame',frame)
    cv.waitKey(0)
    cv.imshow('mask',mask)
    cv.waitKey(0)
    cv.imshow('res',res)
    cv.waitKey(0)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break



    cv.destroyAllWindows()
