# coding:utf-8
import cv2
import sys

# 待检测的图片路径1

#imagepath = r'./test.jpg'
# 获取训练好的人脸的参数数据，这里直接从GitHub上使用默认值
# 现在，我们创建一个 cascade，并用人脸 cascade 初始化。这把人脸 cascade 导入内存，所以它随时可以使用。记住，该 cascade 只是一个包含人脸检测数据的 XML 文件。
face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
print(face_cascade.empty())
# 读取图片
image = cv2.imread('test.jpg')
# 灰度转换的作用就是：转换成灰度的图片的计算强度得以降低
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# 探测图片中的人脸
faces = face_cascade.detectMultiScale(gray,1.1,3)
# scaleFactor调成 1.2能去除错误检测,为每一个级联矩形应该保留的邻近个数，可以理解为一个人周边有几个人脸
# 该函数做的就是检测人脸，是代码核心部分。所以，我们来过一遍选项。DetectMultiScale函数是一个检测物体的通用函数。我们在人脸 cascade上调用它，它检测的就是人脸。第一个选

#项是灰度图片。第二个是 scaleFactor。有的人脸离镜头近，会比其他人脸更大。ScaleFactor对此进行补偿。检测算法使用移动窗口来检测物体。在系统宣布检测到人脸之前，minNeighbors

#会对当前其周围有多少物体进行定义。MinSize给出每个窗口的大小。我用的是这些领域的常用值。现实中，你会拿不同的值试验窗口尺寸、扩展因素等参数，直到找出最比较合适的那一个。
#当该函数认为它找到一张人脸时，会返回一个矩形列表。下一步，我们会进行循环，直到它认为检测出了什么。

print "found{0}faces!".format(len(faces))
for(x,y,w,h) in faces:
#方框
#该函数返回四个值：矩形的 x和 y坐标，以及它的高和宽。我们用这些值和内置的 rectangle函数，画出矩阵
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
#圆形
#cv2.circle(image,((x+x+w)/2,(y+y+h)/2),w/2,(0,255,0),2)
cv2.imshow("Find Faces!",image)
cv2.waitKey(0)
