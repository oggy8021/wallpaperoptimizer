# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_

from WallpaperOptimizer.Imaging.Rectangle import Rectangle

def Rectangle_init_test():
	rect1 = Rectangle()
	rect2 = Rectangle()
	rect1.setSize(1024,768)
	rect2.setSize(1920,1080)
	eq_(rect1.getSize().w, 1024)
	eq_(rect1.getSize().h, 768)
	eq_(rect2.getSize().w, 1920)
	eq_(rect2.getSize().h, 1080)

def Rectangle_square_test():
	rect = Rectangle()
	rect.setSize(1024,768)
	ok_(rect.isSquare())

	rect2 = Rectangle()
	rect2.setSize(1280,1024)
	ok_(rect2.isSquare())

def Rectangle_wide_test():
	rect = Rectangle()
	rect.setSize(1500,844)
	ok_(rect.isWide())

	rect2 = Rectangle()
	rect2.setSize(1920,1080)
	ok_(rect2.isWide())

def Rectangle_dual_test():
	rect = Rectangle()
	rect.setSize(3200,1080)
	ok_(rect.isDual())

def Rectangle_AspectNoMatch_test():
	rect = Rectangle()
	rect.setSize(1152,768)
	eq_(rect.isSquare(), False)

def extends_Bounds_test():
	rect1 = Rectangle()
	rect2 = Rectangle()

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

def Rectangle_contains_test():
	rect1 = Rectangle()
	rect2 = Rectangle()

	rect1.setSize(1024,768)
	rect2.setSize(1920,1080)

	ok_( rect2.contains(rect1) )
	ok_( not rect1.contains(rect2) )

def Rectangle_containsPlusMergin_test():
	rect1 = Rectangle()
	rect2 = Rectangle()

	rect1.setSize(1910,1070)
	rect2.setSize(1920,1080)

	ok_( rect2.containsPlusMergin(rect1, [5,5,5,5]) )
	ok_( not rect1.containsPlusMergin(rect2, [10,10,0,0]) )
