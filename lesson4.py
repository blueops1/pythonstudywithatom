import cv2 as cv

# Load two images
img1 = cv.imread('test.jpg')
img2 = cv.imread('logo1.jpg')
# I want to put logo on top-left corner, So I create a ROI
rows,cols,channels = img2.shape
roi = img1[0:rows, 0:cols ]
# Now create a mask of logo and create its inverse mask also
img2gray = cv.cvtColor(img2,cv.COLOR_BGR2GRAY)
cv.imshow('img2gray',img2gray)
cv.waitKey(0)
ret, mask = cv.threshold(img2gray, 10, 255, cv.THRESH_BINARY)
cv.imshow('mask',mask)
cv.waitKey(0)
mask_inv = cv.bitwise_not(mask)
cv.imshow('mask_inv',mask_inv)
cv.waitKey(0)
# Now black-out the area of logo in ROI
img1_bg = cv.bitwise_and(roi,roi,mask = mask_inv)
cv.imshow('img1_bg',img1_bg)
cv.waitKey(0)
# Take only region of logo from logo image.
img2_fg = cv.bitwise_and(img2,img2,mask = mask)
cv.imshow('img2_fg',img2_fg)
cv.waitKey(0)
# Put logo in ROI and modify the main image
dst = cv.add(img1_bg,img2_fg)
img1[0:rows, 0:cols ] = dst
cv.imshow('res',img1)
cv.waitKey(0)
cv.destroyAllWindows()
