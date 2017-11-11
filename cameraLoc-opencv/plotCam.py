from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.cbook import get_sample_data
from matplotlib._png import read_png
from scipy.ndimage import rotate


def plot3D(x, y, z, roll, pitch, yaw):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	qr = read_png("./images/pattern.png")

	qrLen = 8.8
	xQR, yQR = ogrid[0:qr.shape[0], 0:qr.shape[1]]
	xQR = (xQR * qrLen / 330) - (qrLen / 2)
	yQR = (yQR * qrLen / 330) - (qrLen / 2)
	ax.plot_surface(xQR, yQR, 0, rstride=10, cstride=10, facecolors=qr)


	iphone6 = read_png("./images/iphone6_front.png")
	iPhoneWidth = 6.7
	iPhoneHeight = 13.8
	xiPhone, yiPhone  = ogrid[0:iphone6.shape[0], 0:iphone6.shape[1]]
	xiPhone = (xiPhone * iPhoneWidth / 468) - (iPhoneWidth / 2)
	yiPhone = (yiPhone * iPhoneHeight / 600) - (iPhoneHeight / 2) 
	ax.plot_surface(xiPhone+x, yiPhone+y, z, rstride=30, cstride=30, facecolors=iphone6)


	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('z')
	ax.set_xlim(-50, 50)
	ax.set_ylim(-50, 50)
	ax.set_zlim(0, z+10)
	show()
