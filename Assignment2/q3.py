import numpy as np
import cv2

# load the image, convert it to grayscale, and blur it using gaussian
image = cv2.imread("building_1.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
cv2.imshow("Gray", gray)
cv2.waitKey(0)

# detect edges in the image using canny
edged = cv2.Canny(gray, 100, 550)
cv2.imshow("Edged", edged)
cv2.imwrite('building_1_canny.jpg', edged)
cv2.waitKey(0)

# detect lines aligned to horizontal and vertical axes using houghLines
lines = cv2.HoughLinesP(edged, 1, np.pi/180, 70, 1, 1)
for x in range(0, len(lines)):
    for x1,y1,x2,y2 in lines[x]:
        cv2.line(image, (x1,y1), (x2,y2), (0,0,255), 2)


cv2.imshow('hough',image)
cv2.imwrite('building_1_windows.jpg', image)
cv2.waitKey(0)

