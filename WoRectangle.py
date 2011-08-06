# -*- coding: utf-8 -*-

import math
from WoBounds import WoBounds 

class WoRectangle(WoBounds):

	def __init__(self):
		self.Size = [0, 0]
		WoBounds.__init__(self)

	def getSize(self):
		self.Size = [ self.getWidth(), self.getHeight() ]
		return self.Size

	def setSize(self, w, h):
		self.setWidth(w)
		self.setHeight(h)
		self.Size = [ self.getWidth(), self.getHeight() ]

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
		quotient_w = math.floor(self.Size[0] / widthAs)
		quotient_h = math.floor(self.Size[1] / heightAs)		
		if (quotient_w == quotient_h):
			return True
		else:
			return False
