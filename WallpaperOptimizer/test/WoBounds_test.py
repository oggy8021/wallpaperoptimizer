# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_

from WallpaperOptimizer.Imaging.WoBounds import WoPoint

def point_init_test():
	point1 = WoPoint()
	point2 = WoPoint()
	eq_(point1.x, 0)
	eq_(point1.y, 0)
	eq_(point2.x, 0)
	eq_(point2.y, 0)

def point_distance_test():
	point1 = WoPoint()
	point2 = WoPoint()
	eq_(point1.distanceX(point2), 0)
	eq_(point1.distanceY(point2), 0)


from WoBounds import WoBounds

def Bounds_init_test():
	area1 = WoBounds()
	area2 = WoBounds()
	eq_(area1.start.x, 0)
	eq_(area1.start.y, 0)
	eq_(area1.end.x, 0)
	eq_(area1.end.y, 0)
	eq_(area1.center.x, 0)
	eq_(area1.center.y, 0)
	eq_(area2.start.x, 0)
	eq_(area2.start.y, 0)
	eq_(area2.end.x, 0)
	eq_(area2.end.y, 0)
	eq_(area2.center.x, 0)
	eq_(area2.center.y, 0)

def Bounds_set_WidthHeight_test():
	area1 = WoBounds()
	area2 = WoBounds()

	area1.setWidth(1024)
	area1.setHeight(768)
	area2.setWidth(1920)
	area2.setHeight(1080)
	eq_(area1.getWidth(), 1024)
	eq_(area1.getHeight(), 768)
	eq_(area2.getWidth(), 1920)
	eq_(area2.getHeight(), 1080)

def Bounds_calcCenter_test():
	area1 = WoBounds()
	area2 = WoBounds()

	area1.setWidth(1024)
	area1.setHeight(768)
	area2.setWidth(1920)
	area2.setHeight(1080)

	area1.calcCenter()
	eq_(area1.center.x, 512)
	eq_(area1.center.y, 384)
	eq_(area1.getCenter().x, 512)
	eq_(area1.getCenter().y, 384)
	eq_(area1.center.distanceX(area1.end), area1.center.x)
	eq_(area1.center.distanceY(area1.end), area1.center.y)

	area2.calcCenter()
	eq_(area2.center.x, 960)
	eq_(area2.center.y, 540)
	eq_(area2.getCenter().x, 960)
	eq_(area2.getCenter().y, 540)
	eq_(area2.center.distanceX(area2.end), area2.center.x)
	eq_(area2.center.distanceY(area2.end), area2.center.y)
