# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_

from WallpaperOptimizer.Imaging.WorkSpace import WorkSpace

def WorkSpace_init_test():
	ws = WorkSpace()
	eq_(ws.Size.w, 3200)
	eq_(ws.Size.h, 1080)
	eq_(ws.depth, 24)

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
