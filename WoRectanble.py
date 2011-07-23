#!/usr/bin/env python

#coding: UTF-8

import math

from WoBounds import WoBounds 
#from var_dump import var_dump

class WoRectangle(WoBounds):

	class Size(object):
		w = 0
		h = 0

	def __init__(self):
		WoBounds.__init__(self)

	def getSize(self):
		self.Size.w = self.getWidth()
		self.Size.h = self.getHeight()
		return self.Size

	def setSize(self, w, h):
		self.setWidth(w)
		self.setHeight(h)

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
		quotient_w = math.floor(self.Size.w / widthAs)
		quotient_h = math.floor(self.Size.h / heightAs)		
		if (quotient_w == quotient_h):
			return str(widthAs) + ':' + str(heightAs)
		else:
			return 'No Match: ' + str(quotient_w) + ':' + str(quotient_h)

#///////////////////////////////////////////////////////////////////////////////////// main

if __name__ == "__main__":

#	Rectangle
	rect = WoRectangle()

	rect.setSize(1024,768)

	print rect.getSize().w
	print rect.getSize().h

	print rect.isSquare()
	print rect.isWide()
	print rect.isDual()

#	Rectangle -> Bounds
	print rect.getWidth()
	print rect.getHeight()
	rect.getCenter()
	print rect.center.x
	print rect.center.y

