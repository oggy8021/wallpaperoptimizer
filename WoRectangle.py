# -*- coding: utf-8 -*-

import math
from WoBounds import WoBounds 

class WoRectangle(WoBounds):

	class WoSize(object):
		w = 0
		h = 0

	def __init__(self):
#		self.Size = [0, 0]
		self.Size = WoRectangle.WoSize()
		WoBounds.__init__(self)

	def getSize(self):
#		self.Size = [ self.getWidth(), self.getHeight() ]
		return self.Size

	def setSize(self, w, h):
#		self.Size = [ w, h ]
		self.Size.w = w
		self.Size.h = h
		self.setWidth(w)
		self.setHeight(h)

	def isSquare(self):
		widthAs = 4;
		heightAs = 3;
		if ( not self.checkAspectRatio(widthAs, heightAs) ):
			widthAs = 5;
			heightAs = 4;
			return self.checkAspectRatio(widthAs, heightAs)
		else:
			return True

	def isWide(self):
		widthAs = 16;
		heightAs = 9;
		if ( not self.checkAspectRatio(widthAs, heightAs) ):
			widthAs = 16;
			heightAs = 10;
			return self.checkAspectRatio(widthAs, heightAs)
		else:
			return True

	def isDual(self):
		widthAs = 8;
		heightAs = 2.7;
		return self.checkAspectRatio(widthAs, heightAs)

	def checkAspectRatio(self, widthAs, heightAs, debug=False):
		quotient_w = math.floor(self.Size.w / widthAs)
		quotient_h = math.floor(self.Size.h / heightAs)
		if (quotient_w == quotient_h):
			return True
		else:
			if (debug == True):
				return quotient_h, quotient_w
			else:
				return False

if __name__ == "__main__":
	rect1 = WoRectangle()
	rect2 = WoRectangle()
	rect1.setSize(1920,1080)
	rect2.setSize(1280,1024)
	print rect1.getSize().w
	print rect2.getSize().w
