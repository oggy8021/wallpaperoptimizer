#!/usr/bin/env python

#coding: UTF-8

#from var_dump import var_dump

class WoPoint(object):
	x = None
	y = None

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

class WoBounds(object):
	start = None
	end = None
	center = WoPoint()

	def __init__(self):
		self.start = WoPoint()
		self.end = WoPoint()

	def getWidth(self):
		return self.end.distanceX(self.start)

	def getHeight(self):
		return self.end.distanceY(self.start)

	def setWidth(self, width):
		self.end.x = width

	def setHeight(self, height):
		self.end.y = height

	def getCenter(self):
		self.center.x = self.getWidth() / 2
		self.center.y = self.getHeight() / 2

#///////////////////////////////////////////////////////////////////////////////////// main

if __name__ == "__main__":

#	Point only
	point1 = WoPoint()
	print point1.x
	print point1.y
	point2 = WoPoint()
	print point1.distanceX(point2)
	print point1.distanceY(point2)

#	Bounds create
	area = WoBounds()
	print area.start.x
	print area.start.y
	print area.end.x
	print area.end.y
#	print type(area.center)
	print area.center.x
	print area.center.y

	area.setWidth(1024)
	area.setHeight(768)
	print area.getWidth()
	print area.getHeight()
	area.getCenter()
	print area.center.x
	print area.center.y
