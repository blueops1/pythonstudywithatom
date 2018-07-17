#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
#
#
########################################################################

"""
File: util_voice.py
Author: nechoy()
Date: 2018/07/17 13:11:50
Brief:
"""

import cv2 as cv
import numpy as np

face_cascade = cv.CascadeClassifier('cvdata/haarcascade_frontalface_alt.xml')
eye_cascade = cv.CascadeClassifier('cvdata/haarcascade_eye.xml')

#cap = cv.VideoCapture('source/baby.mp4')
cap = cv.VideoCapture(0)

while (1):
    _,frame = cap.read()
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,3)
    print "found{0}faces!".format(len(faces))
    for(x,y,w,h) in faces:
    #方框
    #该函数返回四个值：矩形的 x和 y坐标，以及它的高和宽。我们用这些值和内置的 rectangle函数，画出矩阵
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    #圆形
    #cv2.circle(image,((x+x+w)/2,(y+y+h)/2),w/2,(0,255,0),2)
    cv.imshow("Find Faces!",frame)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
    elif k == 13:
        cv.imwrite("test1.jpg",frame)
cv.destroyAllWindows()
cap.release()
