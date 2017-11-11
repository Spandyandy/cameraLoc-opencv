import numpy as np
import cv2
import math
from plotCam import plot3D
__author__ = "Junghoo Andy Kim"
#http://danceswithcode.net/engineeringnotes/rotations_in_3d/demo3D/rotations_in_3d_tool.html

def cvtImgToGray(img):
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

def contourApproximation(vert):
	cnt = np.concatenate((vert[0], vert[1], vert[2]))
	#Contour Perimeter of Closed Contour
	epsilon = 0.1*cv2.arcLength(cnt,True)
	#Second argument is epsilon, which is maximum distance from contour to approximated contour. 
	#It is an accuracy parameter. A wise selection of epsilon is needed to get the correct output.
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
	#https://www.quora.com/How-do-I-find-the-4th-point-of-a-parallelogram-in-3D-coordinates
	br = [(-tl[0]+tr[0]+bl[0]), (-tl[1]+tr[1]+bl[1])]
	return [tl, bl, br, tr]

def drawCircles(img, vertices):
	cv2.circle(img,(vertices[0][0],vertices[0][1]),10,(0,0,255),-1)
	cv2.circle(img,(vertices[1][0],vertices[1][1]),10,(255,0,0),-1)
	cv2.circle(img,(vertices[2][0],vertices[2][1]),10,(0,255,0),-1)
	cv2.circle(img,(vertices[3][0],vertices[3][1]),10,(255,255,0),-1)

def getSolvePnPInputs(img, vertices):
	#8.8cm x 8.8cm
	qrLength = 8.8/2
	objectPoints = np.float32([[-qrLength, qrLength,0],
							 [-qrLength, -qrLength,0], 
							 [qrLength, -qrLength,0], 
							 [qrLength, qrLength,0]])

	imagePoints = np.float32(vertices)

	#Camera Matrix A = [fx 0  cx
	#					0  fy cy
	#					0  0  1]
	#fx, fy can be image width, cx and cy can be coordinates of the image center
	height, width = img.shape[:2]
	cameraMatrix = np.float64([[width,0,width/2],
							 [0,width,height/2],
							 [0.0,0.0,1.0]])

	return objectPoints, imagePoints, cameraMatrix

def getPRY(m):
	sy = math.sqrt(m[0][0]*m[0][0] + m[1][0]*m[1][0])
	x = math.atan2(m[1][0], m[0][0])
	y = math.atan2(-m[2][0], sy)
	z = math.atan2(m[2][1], m[2][2])
	return x*180/math.pi, y*180/math.pi, z*180/math.pi

def drawVertices(img, imageNum, vertices):
	drawCircles(img, vertices)
	img = cv2.resize(img, (720,960))
	cv2.imshow(str(imageNum), img)

for imageNum in range(6719, 6727):
	#Step 1 : Open Image
	img = cv2.imread('images/IMG_' + str(imageNum) + '.JPG')
	print("\nImage Number " +  str(imageNum))

	#Step 2 : Convert Image to grayscale, and find countours.
	#cv2.imshow('image', img)
	contours, hierarchy = cvtImgToGray(img)

	#Step 3 : Find 3 contours of the qr code square
	# Actual inner list of hierarchy descriptions
	# If can't detect 3 nested squares, then qr code is not found
	cnts = find3Contours(contours, hierarchy)
	if len(cnts) != 3:
	 	print("QR code not found!")
	 	continue

	# Step 4 : Contour Approximation
	# It approximates a contour shape to another shape with less number of vertices depending upon the precision we specify.
	# Reference : https://docs.opencv.org/3.3.0/dd/d49/tutorial_py_contour_features.html
	approx = contourApproximation(cnts)

	# Step 5 : Calculate vertices' locations
	# From "pattern.png", find top-left, top-right, bottom-left (tl, tr, bl) 
	# Reference : http://answers.opencv.org/question/14188/calc-eucliadian-distance-between-two-single-point/
	vertices = calcVertices(approx)

	# Step 6 : Use solvePnP and Rodrigues to get translation vectors and rotation matrix
	# Get Rotation Vectors and Translation vectors
	# Reference : https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html
	# Reference : http://ksimek.github.io/2013/08/13/intrinsic/
	objectPoints, imagePoints, cameraMatrix = getSolvePnPInputs(img, vertices)
	_, rvec, tvec = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix, np.zeros(4),1)
	rmat, _=cv2.Rodrigues(rvec)
	tvec = -np.dot(rmat.T,tvec)

	# Step 7 : Get Pitch Roll Yaw values from Rotation Matrix
	# Reference : https://d3cw3dd2w32x2b.cloudfront.net/wp-content/uploads/2012/07/euler-angles.pdf
	# https://www.learnopencv.com/rotation-matrix-to-euler-angles/
	yaw, pitch, roll = getPRY(rmat)
	
	print("\nTranslation Vector : \n" +str(tvec))
	print("\nRotation : \n" +str(rmat))
	print("\nRoll : " + str(roll))
	print("Pitch : " + str(pitch))
	print("Yaw : " + str(yaw))
	print("------------------------------------------")

	drawVertices(img, imageNum, vertices)
	plot3D(tvec[0], tvec[1], tvec[2], roll, pitch, yaw)
	cv2.destroyAllWindows()