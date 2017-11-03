import numpy as np
import cv2
from matplotlib import pyplot as plt


#Step 1 : Open Image / Convert Image to GrayScale
img = cv2.imread('images/IMG_6719.JPG')
cv2.namedWindow('image', cv2.WINDOW_NORMAL) 
cv2.imshow('image', img)
#For Debugging
#cv2.imshow('image2', img)


#Step 3 : Convert to Binary


#Step 4 : Canny Edge Detection






#Step 5 : Find Contours .findContours


#Step 6 : 






gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(img,127,255,0)
thresh=cv2.Canny(img,100,200)
cv2.namedWindow('Canny', cv2.WINDOW_NORMAL) 
cv2.imshow('Canny', thresh)
_, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# i=-1
# cv2.drawContours(img,contours,i,(255,0,0),3)

hierarchy = hierarchy[0] # actual inner list of hierarchy descriptions
vertices = []
for i in range(0, len(contours)):
	level = 0
	first_child = hierarchy[i][2]
	while(first_child != -1): 
		first_child = hierarchy[first_child][2]
		level += 1
	if level == 4:
		vertices.append(i)

#If can't detect 3 nested squares, then qr code is not found
if len(vertices) != 3:
	print("Can't detect QR code")
else:
	for i in range(0, 3):
		print (vertices[i])


cv2.namedWindow('image2', cv2.WINDOW_NORMAL) 
cv2.imshow('image2', img)
k = cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()