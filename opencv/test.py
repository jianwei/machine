import cv2 as cv

img = cv.imread("sample.jpeg")

gary_img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

cv.imshow('gary_img', gary_img)

cv.imwrite("gary_img.jpeg",gary_img)

# cv.imshow('read_img', img)

cv.waitKey(20000)

cv.destroyAllWindows()
