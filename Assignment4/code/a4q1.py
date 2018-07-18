import cv2
import scipy.io as sci

font = cv2.FONT_HERSHEY_TRIPLEX
# Read input images
img1 = cv2.imread('../data/test/left/004945.jpg') # 3 cars
img2 = cv2.imread('../data/test/left/004964.jpg') # 3 cars 1 person
img3 = cv2.imread('../data/test/left/005002.jpg') # 3 cars

# Read input matrix dets
mat1 = sci.loadmat('../data/test/results/004945_dets.mat')
mat2 = sci.loadmat('../data/test/results/004964_dets.mat')
mat3 = sci.loadmat('../data/test/results/005002_dets.mat')

car1, car2, car3 = [], [], []
for index in range(len(mat1['dets'][0][0]) + 1):
    car1.append(int(mat1['dets'][0][0][0][index]))

for index in range(len(mat1['dets'][0][0]) + 1):
    car2.append(int(mat1['dets'][0][0][1][index]))

for index in range(len(mat1['dets'][0][0]) + 1):
    car3.append(int(mat1['dets'][0][0][2][index]))

cv2.rectangle(img1, (car1[0], car1[1]), (car1[2], car1[3]), (0, 0, 255), 2)
cv2.rectangle(img1, (car2[0], car2[1]), (car2[2], car2[3]), (0, 0, 255), 2)
cv2.rectangle(img1, (car3[0], car3[1]), (car3[2], car3[3]), (0, 0, 255), 2)
cv2.putText(img1, 'car', (car1[0], car1[1]), font, 1, (0, 0, 255), 2)
cv2.putText(img1, 'car', (car2[0], car2[1]), font, 1, (0, 0, 255), 2)
cv2.putText(img1, 'car', (car3[0], car3[1]), font, 1, (0, 0, 255), 2)

car1, car2, car3, person1 = [], [], [], []
for index in range(len(mat2['dets'][0][0]) + 1):
    car1.append(int(mat2['dets'][0][0][0][index]))

for index in range(len(mat2['dets'][0][0]) + 1):
    car2.append(int(mat2['dets'][0][0][1][index]))

for index in range(len(mat2['dets'][0][0]) + 1):
    car3.append(int(mat2['dets'][0][0][2][index]))

for index in range(len(mat2['dets'][1][0]) + 3):
    person1.append(int(mat2['dets'][1][0][0][index]))

cv2.rectangle(img2, (car1[0], car1[1]), (car1[2], car1[3]), (0, 0, 255), 2)
cv2.rectangle(img2, (car2[0], car2[1]), (car2[2], car2[3]), (0, 0, 255), 2)
cv2.rectangle(img2, (car3[0], car3[1]), (car3[2], car3[3]), (0, 0, 255), 2)
cv2.rectangle(img2, (person1[0], person1[1]), (person1[2], person1[3]), (255, 0, 0), 2)
cv2.putText(img2, 'car', (car1[0], car1[1]), font, 1, (0, 0, 255), 2)
cv2.putText(img2, 'car', (car2[0], car2[1]), font, 1, (0, 0, 255), 2)
cv2.putText(img2, 'car', (car3[0], car3[1]), font, 1, (0, 0, 255), 2)
cv2.putText(img2, 'person', (person1[0], person1[1]), font, 1, (255, 0, 0), 2)

car1, car2, car3 = [], [], []
for index in range(len(mat3['dets'][0][0]) + 1):
    car1.append(int(mat3['dets'][0][0][0][index]))

for index in range(len(mat3['dets'][0][0]) + 1):
    car2.append(int(mat3['dets'][0][0][1][index]))

for index in range(len(mat3['dets'][0][0]) + 1):
    car3.append(int(mat3['dets'][0][0][2][index]))

cv2.rectangle(img3, (car1[0], car1[1]), (car1[2], car1[3]), (0, 0, 255), 2)
cv2.rectangle(img3, (car2[0], car2[1]), (car2[2], car2[3]), (0, 0, 255), 2)
cv2.rectangle(img3, (car3[0], car3[1]), (car3[2], car3[3]), (0, 0, 255), 2)
cv2.putText(img3, 'car', (car1[0], car1[1]), font, 1, (0, 0, 255), 2)
cv2.putText(img3, 'car', (car2[0], car2[1]), font, 1, (0, 0, 255), 2)
cv2.putText(img3, 'car', (car3[0], car3[1]), font, 1, (0, 0, 255), 2)

cv2.imshow ('004945', img1)
cv2.imshow ('004964', img2)
cv2.imshow ('005002', img3)

cv2.imwrite('004945.jpg', img1)
cv2.imwrite('004964.jpg', img2)
cv2.imwrite('005002.jpg', img3)
cv2.waitKey()
