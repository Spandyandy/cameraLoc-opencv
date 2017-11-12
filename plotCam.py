from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.cbook import get_sample_data
from matplotlib._png import read_png
import math
__author__ = "Junghoo Andy Kim"

def plot3D(tvec, imageNum, loc):
	x = tvec[0]
	y = tvec[1]
	z = tvec[2]
	qrLen = 8.8


	# Setup
	fig = plt.figure()
	fig.suptitle("Image_" + str(imageNum) + " | Drag to Rotate!")
	ax = fig.add_subplot(111, projection='3d')


	# QR Code Image lying on location (0,0,0)
	qr = read_png("./images/pattern.png")
	xQR, yQR = ogrid[0:qr.shape[0], 0:qr.shape[1]]
	xQR = (xQR * qrLen / 330) - (qrLen / 2)
	yQR = (yQR * qrLen / 330) - (qrLen / 2)
	ax.plot_surface(xQR, yQR, 0, rstride=20, cstride=20, facecolors=qr)


	# Location of Camera and its direction
	ax.scatter(x, y, z, marker='o', color='red')
	ax.plot([x,loc[0]-x],[y,loc[1]-y],zs=[z,loc[2]-z], label='Camera Angle')


	# Axis range
	ax.plot([-50, 50], [0,0], [0,0], label='x')
	ax.plot([0,0], [-50, 50], [0,0], label='y')
	ax.legend()	
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('z')
	ax.set_xlim(-50, 50)
	ax.set_ylim(-50, 50)
	ax.set_zlim(0, z+10)

	show()
