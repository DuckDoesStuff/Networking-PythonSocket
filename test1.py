import cv2

path = './temp/TA_in_a_chest.png'
img = cv2.imread(path)

cv2.imshow('Display Image', img)
cv2.waitKey(0)