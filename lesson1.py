print 'lesson1!'
print 'new branch of atom'
import cv2 as cv
img = cv.imread("logo.jpg",0)
#result = cv.imread("test.jpg")
#print img
#cv.Canny(img,result,50,150)
#cv.imwrite("test1.jpg",result)
#cv.namedWindow("aaa",0)
cv.imshow("aaa",img)
k = cv.waitKey(0)
if k == 27:
    cv.destroyAllWindows()
elif k == ord("s"):
    cv.imwrite("logo1.jpg",img)
    cv.destroyAllWindows()
