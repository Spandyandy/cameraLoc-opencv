# Camera Localization 

**Author : Junghoo Kim (Andy)**

**Languages / Packages Used** : Python3, OpenCV2, pylab, matplotlib, math, numpy

**DroneDeploy Coding Challenge**

## Summary

A number of images taken from different positions and orientations with an iPhone 6 is given. Each image is the view of a pattern on a flat surface. The original pattern that was photographed is 8.8cm x 8.8cm and is included in the zip file. Write a Python program that will visualize (i.e. generate a graphic) where the camera was when each image was taken and how it was posed, relative to the pattern.

Assume that the pattern is at 0,0,0 in some global coordinate system and are thus looking for the x, y, z and yaw, pitch, roll of the camera that took each image. Please submit a link to a Github repository contain the code for your solution. Readability and comments are taken into account too. You may use 3rd party libraries like OpenCV and Numpy.

## How to Run

pip install opencv-python

python -B cameraLoc.py

## Steps

**Step 1** : Open Image

**Step 2** : Convert Image to grayscale, and find countours.

**Step 3** : Find 3 contours of the qr code square

**Step 4** : Contour Approximation
The approximated curve for epsilon = 10% of arc length

**Step 5** : Calculate vertices' locations
From "pattern.png", find top-left, top-right, bottom-left, bottom-right (tl, tr, bl, br)

**Step 6** : Use solvePnP and Rodrigues to get translation vectors and rotation matrix
![transf](https://docs.opencv.org/2.4/_images/math/803e522ec37bc5bc609c0ef08373a350a819fc15.png)

fx, fy can be image width, cx and cy can be coordinates of the image center

**Step 7** : Get Roll, Pitch, Yaw values from Rotation Matrix

**Step 8** : Print data, show image, plot 

## Tests 

<img src="https://github.com/Spandyandy/cameraLoc-opencv/blob/master/images/IMG_6719.JPG" alt="IMG_6719" width="400">

I tested with the first image (IMG_6719).

My program's output is following:

Image Number 6719

X : 27.1337479271

Y : -34.9468293386

Z : 56.9243043284 

Roll : 148.68643550952663

Pitch : 20.37632648002931

Yaw : 30.813083452658223

<img src="https://github.com/Spandyandy/cameraLoc-opencv/blob/master/steps/1.jpg" alt="Step_1" width="400">

First, I printed the QR code and placed it on "(0, 0, 0)"
<br><br>

<img src="https://github.com/Spandyandy/cameraLoc-opencv/blob/master/steps/2.jpg" alt="Step_2" width="400">

I placed my phone camera on (0, 0, 0). I was not sure about the initial orientation. 
<br><br>

<img src="https://github.com/Spandyandy/cameraLoc-opencv/blob/master/steps/3.jpg" alt="Step_3" width="400">

I translated phone 27.13 cm to the x-axis.
<br><br>

<img src="https://github.com/Spandyandy/cameraLoc-opencv/blob/master/steps/4.jpg" alt="Step_4" width="400">

I translated phone -34.95 cm to the y-axis.
<br><br>

<img src="https://github.com/Spandyandy/cameraLoc-opencv/blob/master/steps/5.jpg" alt="Step_5" width="400">

I translated phone 56.9243 cm to the z-axis.
Here we can see that this was the location where the image was taken.
<br><br>

<img src="https://github.com/Spandyandy/cameraLoc-opencv/blob/master/steps/6.jpg" alt="Step_6" width="400">

I rotated my phone around x-axis (Roll) 148.68 degree. 
<br><br>

<img src="https://github.com/Spandyandy/cameraLoc-opencv/blob/master/steps/7.jpg" alt="Step_7" width="400">
 
I rotated my phone around y-axis (Pitch) 20.38 degree.
<br><br>

<img src="https://github.com/Spandyandy/cameraLoc-opencv/blob/master/steps/8.jpg" alt="Step_8" width="400">

I rotated my phone around z-axis (Yaw) 30.81 degree. 
<br><br>


<img src="https://github.com/Spandyandy/cameraLoc-opencv/blob/master/steps/9.jpg" alt="Step_9" width="400">

The camera screen of my phone seems to match the given input image! (Well, pretty close)
<br><br>

![Calculations](https://github.com/Spandyandy/cameraLoc-opencv/blob/master/steps/calculations.jpg)

This is how to find the point where the camera was looking at. (Focal Point)

But then I realized matrix multiplication of rotation matrix and translation vector gives exactly same thing

So I decided to use numpy.matmul(rmat, tvec) 
<br><br>

![Plot](https://github.com/Spandyandy/cameraLoc-opencv/blob/master/output/plot6719.png)

QR code is on the (0, 0, 0), and the red dot is where the camera lens was.

The red line represents the angle/orientation camera was pointing. 

The end of the line below z-axis is where the focal point was. 
<br><br>

## Different Approach

My first approach to this problem was to use Canny Edge detection.

![Canny](https://github.com/Spandyandy/cameraLoc-opencv/blob/master/steps/canny.jpg "Canny Edge Detection")

Although it looks cool, I realized it was not really necessary, because I decided to convert image to grayscale and threshold to find contours instead.


## Reference
**Step 4** : https://docs.opencv.org/3.3.0/dd/d49/tutorial_py_contour_features.html

**Step 5** : http://answers.opencv.org/question/14188/calc-eucliadian-distance-between-two-single-point/
             https://www.quora.com/How-do-I-find-the-4th-point-of-a-parallelogram-in-3D-coordinates
             
**Step 6** : https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html

**Step 7** : https://d3cw3dd2w32x2b.cloudfront.net/wp-content/uploads/2012/07/euler-angles.pdf
             https://www.learnopencv.com/rotation-matrix-to-euler-angles/

**Test** : http://danceswithcode.net/engineeringnotes/rotations_in_3d/demo3D/rotations_in_3d_tool.html
