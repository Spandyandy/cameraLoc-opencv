# Camera Localization 

Junghoo Kim (Andy)

Languages / Packages Used : Python3, OpenCV2, pylab, matplotlib, math, numpy

# Summary

A number of images taken from different positions and orientations with an iPhone 6 is given. Each image is the view of a pattern on a flat surface. The original pattern that was photographed is 8.8cm x 8.8cm and is included in the zip file. Write a Python program that will visualize (i.e. generate a graphic) where the camera was when each image was taken and how it was posed, relative to the pattern.

Assume that the pattern is at 0,0,0 in some global coordinate system and are thus looking for the x, y, z and yaw, pitch, roll of the camera that took each image. Please submit a link to a Github repository contain the code for your solution. Readability and comments are taken into account too. You may use 3rd party libraries like OpenCV and Numpy.

# How to Run

Type 'python -B cameraLoc.py'

# Step By Step / Difficulties

First, I tried to use Canny Edge detection.

![alt text](https://github.com/Spandyandy/cameraLoc-opencv/blob/master/steps/canny.jpg "Canny Edge Detection")

![Canny](/stepbystep/canny.jpg)

Format: ![Alt Text]()

