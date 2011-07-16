#!/usr/bin/env python

#coding: UTF-8

from PIL import Image

class ImgFile:
	def __init__(self, imgfile):
		im = Image.open(imgfile)
		self.x = im.size[0]
		self.y = im.size[1]
