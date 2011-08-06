# -*- coding: utf-8 -*-

class WoPoint(object):
	def __init__(self):
		self.x = 0
		self.y = 0

	def distanceX(self, other):
		if (self.x >= other.x):
			return self.x - other.x
		else:
			return other.x - self.x

	def distanceY(self, other):
		if (self.y >= other.y):
			return self.y - other.y
		else:
			return other.y - self.y

	def distance(self, other):
		pass

class WoBounds(object):
	def __init__(self):
		self.start = WoPoint()
		self.end = WoPoint()
		self.center = WoPoint()

	def getWidth(self):
		return self.end.distanceX(self.start)

	def getHeight(self):
		return self.end.distanceY(self.start)

	def setWidth(self, width):
		self.end.x = width

	def setHeight(self, height):
		self.end.y = height

	def calcCenter(self):
		self.center.x = self.getWidth() / 2
		self.center.y = self.getHeight() / 2

	def getCenter(self):
		return self.center

