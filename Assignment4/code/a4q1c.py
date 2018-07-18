import cv2
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

K =  [[721.5377,    0, 609.5593],
      [  0,  721.5377, 172.8540],
      [  0,    0,  1.0000]]
  
baseline = 0.5327
f = 721.5377
px = 609.5593
py = 172.8540

real_left = cv2.imread('../data/test/left/004945.jpg')
real_left = cv2.cvtColor(real_left, cv2.COLOR_BGR2GRAY);
real_right = cv2.imread('../data/test/right/004945.jpg')
real_right = cv2.cvtColor(real_right, cv2.COLOR_BGR2GRAY);
img = cv2.imread('../data/test/results/004945_left_disparity.png')
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
disparity = np.double(gray_image)
disparity[disparity < 1] = 1
depth = (baseline * f) / disparity

Xs = []
Ys = []
Zs = []
colormap = []

for x in range(0, depth.shape[1]):
      for y in range(0, depth.shape[0]):
            bigX = (depth[y,x] * (x - px)) / f
            bigY = (depth[y,x] * (y - py)) / f
            Xs.append(bigX)
            Ys.append(bigY)
            Zs.append(depth[y,x])

p = np.array([Xs, Ys, Zs])
p = p.transpose()

print real_left.shape
print real_right.shape
print depth.shape

cv2.imshow('depth', np.hstack((real_left, real_right, disparity)))
cv2.waitKey(0)

