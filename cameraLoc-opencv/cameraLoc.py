import numpy as np
import cv2
#https://www.learnopencv.com/rotation-matrix-to-euler-angles/

#Step 1 : Open Image and resize image by approximately width/4, height/4
for imageNum in range(6719, 6727):
	img = cv2.imread('images/IMG_' + str(imageNum) + '.JPG')
	img = cv2.resize(img, (600,800))
	print("\nImage Number " +  str(imageNum))
	#Step 2 : Convert Image to grayscale, and find countours.
	#cv2.imshow('image', img)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray,200,255,0)
	img2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	#Step 3 : Find 3 vertices of the qr code square
	# actual inner list of hierarchy descriptions
	hierarchy = hierarchy[0] 
	vert = []
	for i in range(0, len(contours)):
		level = 0
		first_child = hierarchy[i][2]
		while(first_child != -1): 
			first_child = hierarchy[first_child][2]
			level += 1
		#There are three squares on QR code, and each has two nested squares (children) 
		if level == 2:
			vert.append(contours[i])

	#If can't detect 3 nested squares, then qr code is not found
	if len(vert) != 3:
		print("QR code not found!")
	else :
		cnt = np.concatenate((vert[0], vert[1], vert[2]))
		#https://docs.opencv.org/3.3.0/dd/d49/tutorial_py_contour_features.html
		#Contour Perimeter of Closed Contour
		epsilon = 0.1*cv2.arcLength(cnt,True)
		#Second argument is epsilon, which is maximum distance from contour to approximated contour. 
		#It is an accuracy parameter. A wise selection of epsilon is needed to get the correct output.
		approx = cv2.approxPolyDP(cnt, epsilon, True)

		#From "pattern.png", find top-left, top-right, bottom-left (tl, tr, bl) 
		#http://answers.opencv.org/question/14188/calc-eucliadian-distance-between-two-single-point/
		vertex = []
		line = []
		for i in range(0, 3):
			vertex.append(approx[i][0])
			#Print vertices' Locations, and mark them on the image 
			print (vertex[i])
			cv2.circle(img,(vertex[i][0],vertex[i][1]),2,(0,0,255),-1)
		for i in range(0, 3):
			line.append(cv2.norm(vertex[i]-vertex[(i+1)%3]))

		indexMax = line.index(max(line[0], line[1], line[2]))
		tl = vertex[(indexMax+2)%3]
		tr = vertex[(indexMax+1)%3]
		bl = vertex[indexMax]
		cv2.circle(img,(tl[0],tl[1]),2,(255,0,0),-1)
		cv2.circle(img,(tr[0],tr[1]),2,(0,255,0),-1)
		print("Top-Left : " + str(tl))

	cv2.imshow(str(imageNum), img)
k = cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()