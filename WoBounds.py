#!/usr/bin/env python

#coding: UTF-8

#from var_dump import var_dump

class WoPoint(object):
	x = None
	y = None

	def __init__(self):
		self.x = 0
		self.y = 0

class WoBounds(object):
	start = None
	end = None
	center = WoPoint()

	def __init__(self):
		self.start = WoPoint()
		self.end = WoPoint()

	def getWidth(self):
		return self.end.x - self.start.x

	def getHeight(self):
		return self.end.y - self.start.y

	def setWidth(self, width):
		self.end.x = width

	def setHeight(self, height):
		self.end.y = height

	def getCenter(self):
		self.center.x = self.getWidth / 2
		self.center.y = self.getHeight / 2


#///////////////////////////////////////////////////////////////////////////////////// main

if __name__ == "__main__":

#	Point only
	point = WoPoint()
	print point.x
	print point.y

#	Bounds create
	area = WoBounds()
	print area.start.x
	print area.start.y
	print area.end.x
	print area.end.y
