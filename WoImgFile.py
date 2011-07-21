#!/usr/bin/env python

#coding: UTF-8

from PIL import Image
from ImgObject import ImgObject
from var_dump import var_dump

class ImgFile(ImgObject):

	class size(object):
		w = 0
		h = 0

	def __init__(self):
		self._img=img.new()

	def __init__(self,img):
		self._img=img

	def loadImgFile(self, imgfile):
		ImgObject.img(Image.open(imgfile))


#///////////////////////////////////////////////////////////////////////////////////// main

if __name__ == "__main__":
	file = '1500x844.jpg'	#16:9
#	file = '1000x800.jpg'	#No Match
#	file = '2560x1920.jpg' #4:3

	img = ImgFile(Image.new)
	img = ImgFile(Image.open(file))

	print type(img)
	var_dump(img)

#	img.setGeometry()

#	print img.getGeometry().w
#	print img.getGeometry().h

#	print img.isSquare()
#	print img.isWide()
#	print img.isDual()
