import numpy as np
import cv2
import math
from plotCam import plot3D 
__author__ = "Junghoo Andy Kim"

def cvtFindContours(img):
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray,200,255,0)
	_, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	return contours, hierarchy

def find3Contours(contours, hierarchy):
	hierarchy = hierarchy[0]
	cnts = []
	for i in range(0, len(contours)):
		level = 0
		first_child = hierarchy[i][2]
		while(first_child != -1): 
			first_child = hierarchy[first_child][2]
			level += 1
		#There are three squares on QR code, and each has two nested squares (children) 
		if (level == 2):
			cnts.append(contours[i])
	return cnts

#Contour Perimeter of Closed Contour
#Epsilon is the maximum distance from contour to approximated contour. 
def contourApproximation(vert):
	cnt = np.concatenate((vert[0], vert[1], vert[2]))
	epsilon = 0.1*cv2.arcLength(cnt,True)
	approx = cv2.approxPolyDP(cnt, epsilon, True)
	return approx

def calcVertices(approx):
	vertex = []
	line = []
	for i in range(0, 3):
		vertex.append(approx[i][0])
	for i in range(0, 3):
		line.append(cv2.norm(vertex[i]-vertex[(i+1)%3]))
	indexMax = line.index(max(line[0], line[1], line[2]))
	tl = vertex[(indexMax+2)%3]
	tr = vertex[(indexMax+1)%3]
	bl = vertex[indexMax]
	if np.cross(tl-tr,tl-bl) < 0:
		tr,bl = bl,tr
	#Find 4th vertex 
	br = [(-tl[0]+tr[0]+bl[0]), (-tl[1]+tr[1]+bl[1])]
	return [tl, bl, br, tr]

def getSolvePnPInputs(img, vertices):
	#8.8cm x 8.8cm
	qrLength = 8.8/2
	objectPoints = np.float32([[-qrLength, qrLength,0],
							 [-qrLength, -qrLength,0], 
							 [qrLength, -qrLength,0], 
							 [qrLength, qrLength,0]])
	imagePoints = np.float32(vertices)
	height, width = img.shape[:2]
	cameraMatrix = np.float64([[width,0,width/2],
							 [0,width,height/2],
							 [0.0,0.0,1.0]])
	return objectPoints, imagePoints, cameraMatrix

def getRPY(m):
	sy = math.sqrt(m[0][0]*m[0][0] + m[1][0]*m[1][0])
	x = math.atan2(m[1][0], m[0][0])
	y = math.atan2(-m[2][0], sy)
	z = math.atan2(m[2][1], m[2][2])
	return z*180/math.pi, y*180/math.pi, x*180/math.pi

def showImg(img, imageNum, vertices):
	for i in range(0,4):
		cv2.circle(img,(vertices[i][0],vertices[i][1]),20,((i+2)%4*80,(i+1)%4*80,i*80),-1)
	img = cv2.resize(img, (600,800))
	cv2.imshow(str(imageNum), img)

def printInfo(tvec, roll, pitch, yaw):
	print("X : " +str(tvec[0][0]))
	print("Y : " +str(tvec[1][0]))
	print("Z : " +str(tvec[2][0]))
	print("Roll : " + str(roll) )
	print("Pitch : " + str(pitch))
	print("Yaw : " + str(yaw))
	print("------------------------------------------\n")



for imageNum in range(6719, 6728):

	#Step 1 : Open Image
	img = cv2.imread('images/IMG_' + str(imageNum) + '.JPG')
	print("\nImage Number " +  str(imageNum))


	#Step 2 : Convert Image to grayscale, and find countours.
	contours, hierarchy = cvtFindContours(img)


	#Step 3 : Find 3 contours of the qr code square
	# Qr code is not found, if # of nested contours != 3
	cnts = find3Contours(contours, hierarchy)
	if len(cnts) != 3:
	 	print("QR code not found!")
	 	continue


	# Step 4 : Contour Approximation
	# The approximated curve for epsilon = 10% of arc length
	approx = contourApproximation(cnts)


	# Step 5 : Calculate vertices' locations
	# From "pattern.png", find top-left, top-right, bottom-left, bottom-right (tl, tr, bl, br) 
	vertices = calcVertices(approx)


	# Step 6 : Use solvePnP and Rodrigues to get translation vectors and rotation matrix
	# Camera Matrix = [[fx, 0, cx], [0, fy, cy], [0, 0, 1]]
	# fx, fy can be image width, cx and cy can be coordinates of the image center
	objectPoints, imagePoints, cameraMatrix = getSolvePnPInputs(img, vertices)
	_, rvec, tvec = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix, np.zeros(4),1)
	rmat, _=cv2.Rodrigues(rvec)
	tvec = -np.dot(rmat.T, tvec)


	# Step 7 : Get Roll, Pitch, Yaw values from Rotation Matrix
	roll, pitch, yaw = getRPY(rmat)


	# Step 8 : Print data, show image, plot 
	# Matrix multiplication of rotation matrix and translation vector gives the direction of camera
	printInfo(tvec, roll, pitch, yaw)
	showImg(img, imageNum, vertices)
	plot3D(tvec, imageNum, np.matmul(rmat,tvec))
	cv2.destroyAllWindows()