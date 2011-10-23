# -*- coding: utf-8 -*-

import math
from WallpaperOptimizer.Imaging.WoBounds import WoBounds

class WoRectangle(WoBounds):

	class WoSize(object):
		w = 0
		h = 0

	def __init__(self):
		self.Size = WoRectangle.WoSize()
		WoBounds.__init__(self)

	def getSize(self):
		return self.Size

	def setSize(self, w, h):
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

	def checkAspectRatio(self, widthAs, heightAs):
		quotient_w = math.floor(self.Size.w / widthAs)
		quotient_h = math.floor(self.Size.h / heightAs)
		if (quotient_w == quotient_h):
			return True
		else:
			return False

	def contains(self, other):
		if ( self.Size.w >= other.Size.w and self.Size.h >= other.Size.h ):
			return True
		else:
			return False

	def containsPlusMergin(self, other, mergin):
		if ( self.Size.w >= (other.Size.w + mergin[0] + mergin[1])
			 and self.Size.h >= (other.Size.h  + mergin[2] + mergin[3])):
			return True
		else:
			return False

