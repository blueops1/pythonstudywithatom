#coding:utf-8
import cv2 as cv
import numpy as np

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv.VideoCapture(0)

while (1):
    _,frame = cap.read()
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.1,3)
    print "found{0}faces!".format(len(faces))
    for(x,y,w,h) in faces:
    #方框
    #该函数返回四个值：矩形的 x和 y坐标，以及它的高和宽。我们用这些值和内置的 rectangle函数，画出矩阵
     cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    #圆形
    #cv2.circle(image,((x+x+w)/2,(y+y+h)/2),w/2,(0,255,0),2)
    cv.imshow("Find Faces!",frame)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()
cap.release()
