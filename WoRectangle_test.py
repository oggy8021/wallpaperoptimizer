# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_

from WoRectangle import WoRectangle

def Rectangle_init_test():
	rect1 = WoRectangle()
	rect2 = WoRectangle()
	rect1.setSize(1024,768)
	rect2.setSize(1920,1080)
	eq_(rect1.getSize()[0], 1024)
	eq_(rect1.getSize()[1], 768)
	eq_(rect2.getSize()[0], 1920)
	eq_(rect2.getSize()[1], 1080)

def Rectangle_square_test():
	rect = WoRectangle()
	rect.setSize(1024,768)
	ok_(rect.isSquare())

	rect2 = WoRectangle()
	rect2.setSize(1280,1024)
	ok_(rect2.isSquare())

def Rectangle_wide_test():
	rect = WoRectangle()
	rect.setSize(1500,844)
	ok_(rect.isWide())

	rect2 = WoRectangle()
	rect2.setSize(1920,1080)
	ok_(rect2.isWide())

def Rectangle_dual_test():
	rect = WoRectangle()
	rect.setSize(3200,1080)
	ok_(rect.isDual())

def Rectangle_AspectNoMatch_test():
	rect = WoRectangle()
	rect.setSize(1152,768)
	eq_(rect.isSquare(), False)

def extends_Bounds_test():
	rect1 = WoRectangle()
	rect2 = WoRectangle()

	rect1.setSize(1024,768)
	rect2.setSize(1920,1080)

	eq_(rect1.getWidth(), 1024)
	eq_(rect1.getHeight(), 768)
	eq_(rect2.getWidth(), 1920)
	eq_(rect2.getHeight(), 1080)

	rect1.calcCenter()
	eq_(rect1.center.x, 512)
	eq_(rect1.center.y, 384)
	rect2.calcCenter()
	eq_(rect2.center.x, 960)
	eq_(rect2.center.y, 540)
