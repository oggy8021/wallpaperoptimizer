#!/usr/bin/env python

#coding: UTF-8

from PIL import Image

class ImgFile:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.im = None

	def readImage(self, imgfile):
		self.im = Image.open(imgfile)
#		setGeometry()
#		return getGeometry()

	def setGeometry(self):
		self.x = self.im.size[0]
		self.y = self.im.size[1]

	def getGeometry(self):
		return self.im.size


if __name__ == "__main__":
	file = '/home/katsu/Wallpaper/transformers2_00101.jpg'

	img = ImgFile()
	img.readImage(file)
	img.setGeometry()
	print img.getGeometry()
#	img.im.show()
