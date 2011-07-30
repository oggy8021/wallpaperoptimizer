
from nose.tools import ok_, eq_

from WoBounds import WoPoint

def point1_init_test():
	point1 = WoPoint()
	eq_(point1.x, 0)
	eq_(point1.y, 0)

def point2_init_test():
	point2 = WoPoint()
	eq_(point2.x, 0)
	eq_(point2.y, 0)

def point_distance_test():
	point1 = WoPoint()
	point2 = WoPoint()
	eq_(point1.distanceX(point2), 0)
	eq_(point1.distanceY(point2), 0)

from WoBounds import WoBounds

def Bounds_init_test():
	area = WoBounds()
	eq_(area.start.x, 0)
	eq_(area.start.y, 0)
	eq_(area.end.x, 0)
	eq_(area.end.y, 0)
	eq_(area.center.x, 0)
	eq_(area.center.y, 0)

def Bounds_set_size_test():
	area = WoBounds()

	area.setWidth(1024)
	area.setHeight(768)
	eq_(area.getWidth(), 1024)
	eq_(area.getHeight(), 768)

def Bounds_calcCenter_test():
	area = WoBounds()

	area.setWidth(1024)
	area.setHeight(768)

	area.calcCenter()
	eq_(area.center.x, 512)
	eq_(area.center.y, 384)
