#!/usr/bin/env python

#coding: UTF-8

from PIL import Image
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


#///////////////////////////////////////////////////////////////////////////////////// main

if __name__ == "__main__":
	file = '/home/katsu/Wallpaper/transformers2_00101.jpg'

	imgObj = ImgObject(Image.open(file))

	imgObj.setGeometry()

	print imgObj.getGeometry().w
	print imgObj.getGeometry().h
