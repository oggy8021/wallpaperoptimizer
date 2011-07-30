# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_

from WoRectangle import WoRectangle

def Rectangle_init_test():
	rect = WoRectangle()
	rect.setSize(1024,768)
	eq_(rect.getSize().w, 1024)
	eq_(rect.getSize().h, 768)

def Rectangle_square_test():
	rect = WoRectangle()
	rect.setSize(1024,768)
#	rect.getSize()
	ok_(rect.isSquare())

def Rectangle_wide_test():
	rect = WoRectangle()
	rect.setSize(1500,844)
#	rect.getSize()
	ok_(rect.isWide())

def Rectangle_dual_test():
	rect = WoRectangle()
	rect.setSize(3200,1080)
#	rect.getSize()
	ok_(rect.isDual())

def Rectangle_AspectNoMatch_test():
	rect = WoRectangle()
	rect.setSize(1152,768)
	eq_(rect.isSquare(), False)

def extends_Bounds_test():
	rect = WoRectangle()3200
	rect.setSize(1024,768)
#	rect.getSize()
	eq_(rect.getWidth(), 1024)
	eq_(rect.getHeight(), 768)

	rect.calcCenter()
	eq_(rect.center.x, 512)
	eq_(rect.center.y, 384)
