import cv2 as cv

# Load two images
img1 = cv.imread('test.jpg')
img2 = cv.imread('logo.png')

# I want to put logo on top-left corner, So I create a ROI
rows,cols,channels = img2.shape
print(rows)
print(cols)
print(img2.item(0,0,1))
for x in range(0,rows):
    for y in range(0,cols):
        if img2.item(x,y,0) < 240:
            if img2.item(x,y,1) < 240:
                if img2.item(x,y,2) <240:
                    img2.itemset((x,y,0),0)
                    img2.itemset((x,y,1),0)
roi = img1[0:rows, 0:cols ]
# Now create a mask of logo and create its inverse mask also
img2gray = cv.cvtColor(img2,cv.COLOR_BGR2GRAY)
cv.imshow('img2gray',img2gray)
cv.waitKey(0)
ret, mask = cv.threshold(img2gray, 38, 245, cv.THRESH_BINARY)
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
