#!/usr/bin/env python

#coding: UTF-8

from PIL import Image
import math
from var_dump import var_dump

class ImgObject(Image.Image):

	class size(object):
		w = 0
		h = 0

	def __init__(self,img):
		self._img=img
#		print type(self._img)

	def setGeometry(self):
		self.size.w = self._img.size[0]
		self.size.h = self._img.size[1]

	def getGeometry(self):
		return self.size

	def isSquare(self):
		widthAs = 4;
		heightAs = 3;
		return self.checkAspectRatio(widthAs, heightAs)

	def isWide(self):
		widthAs = 16;
		heightAs = 9;
		return self.checkAspectRatio(widthAs, heightAs)

	def isDual(self):
		widthAs = 8;
		heightAs = 2.7;
		return self.checkAspectRatio(widthAs, heightAs)

	def checkAspectRatio(self, widthAs, heightAs):
		quotient_w = math.floor(self.size.w / widthAs)
		quotient_h = math.floor(self.size.h / heightAs)		
		if (quotient_w == quotient_h):
			return str(widthAs) + ':' + str(heightAs)
		else:
			return 'No Match: ' + str(quotient_w) + ':' + str(quotient_h)

#///////////////////////////////////////////////////////////////////////////////////// main

if __name__ == "__main__":
	file = '1500x844.jpg'	#16:9
#	file = '1000x800.jpg'	#No Match
#	file = '2560x1920.jpg' #4:3

	imgObj = ImgObject(Image.open(file))

	imgObj.setGeometry()

	print imgObj.getGeometry().w
	print imgObj.getGeometry().h

	print imgObj.isSquare()
	print imgObj.isWide()
	print imgObj.isDual()

