#!/usr/bin/env python

#coding: UTF-8

from PIL import Image
from WoRectangle import WoRectangle
#from var_dump import var_dump

class WoImgFile(WoRectangle, Image.Image):

	def __init__(self,file):
		self._img = Image.open(file)
		print self._img.size[0]
		print self._img.size[1]
		self.setSize(self._img.size[0], self._img.size[1])

	def show(self):
		return self._img.show()

#///////////////////////////////////////////////////////////////////////////////////// main

if __name__ == "__main__":
	file = '../1500x844.jpg'	#16:9
#	file = '../1000x800.jpg'	#No Match
#	file = '../2560x1920.jpg' #4:3

	img = WoImgFile(file)

#	print type(img)
#	print dir(img)

#	img.setGeometry()

#	print img.getGeometry().w
#	print img.getGeometry().h

#	print img.isSquare()
#	print img.isWide()
#	print img.isDual()
