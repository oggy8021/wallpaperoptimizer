# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_

from WallpaperOptimizer.WorkSpace import WorkSpace

def WorkSpace_init_test():
	ws = WorkSpace()
	eq_(ws.Size.w, 3200)
	eq_(ws.Size.h, 1080)
	eq_(ws.depth, 24)
	eq_(ws.getDepth(), 24)

def WorkSpace_Inner_Screen_test():
	ws = WorkSpace()
	ws.lScreen.setSize(1920, 1080)
	ws.rScreen.setSize(1024, 768)

	eq_(ws.lScreen.getSize().w, 1920)
	eq_(ws.lScreen.getSize().h, 1080)
	eq_(ws.lScreen.isSquare(), False)
	eq_(ws.lScreen.isWide(), True)

	eq_(ws.rScreen.getSize().w, 1024)
	eq_(ws.rScreen.getSize().h, 768)
	eq_(ws.rScreen.isSquare(), True)
	eq_(ws.rScreen.isWide(), False)

	eq_(ws.getScreenSize(), ((1920,1080), (1024,768)))

def WorkSpace_marugoto_Screen_test():
	ws = WorkSpace()
	ws.setScreenSize([1920,1080], [1280,1024])
	eq_(ws.getScreenSize(), ((1920,1080), (1280,1024)))

def WorkSpace_compareToScreen1_list_test():
	ws = WorkSpace()
	ws.setScreenSize([1920, 1080], [1280,1024])
	eq_(ws.compareToScreen(), True)

def WorkSpace_compareToScreen1_tuple_test():
	ws = WorkSpace()
	ws.setScreenSize((1920, 1080), (1280,1024))
	eq_(ws.compareToScreen(), True)

def WorkSpace_compareToScreen2_test():
	ws = WorkSpace()
	ws.setScreenSize([1920, 1080], [1920,1080])
	eq_(ws.compareToScreen(), False)

def WorkSpace_setAttrScreenType_test():
	ws = WorkSpace()
	ws.setScreenSize([1920, 1080], [1280,1024])
	ws.setBool(True, True)
	ws.setAttrScreenType()
	eq_(ws.lScreen.displayType, 'wide')
	eq_(ws.rScreen.displayType, 'square')


def WorkSpace_Screen_undefine_test():
	ws = WorkSpace()
	ws.setScreenSize([1920, 1080], [0,0])
	ws.setBool(True, False)
	ws.setAttrScreenType()
	ok_(hasattr(ws.lScreen, 'displayType'))
	ok_(not hasattr(ws.rScreen, 'displayType'))


