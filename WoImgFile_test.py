# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_

from WoImgFile import WoImgFile

def WoImgFile_init_no_param_test():
	Img = WoImgFile()
	eq_(Img.getSize()[0], 5)

def WoImgFile_load_square_test():
	file = '../2560x1920.jpg' #4:3
	Img = WoImgFile(file)
	eq_(Img.getSize()[0], 2560)
	eq_(Img.getSize()[1], 1920)
	ok_( Img.isSquare() )
	ok_( not Img.isWide() )
	ok_( not Img.isDual() )
	Img.calcCenter()
	eq_(Img.getCenter().x, 1280)
	eq_(Img.getCenter().y, 960)

def WoImgFile_load_wide_test():
	file = '../1500x844.jpg'	#16:9
	Img = WoImgFile(file)
	eq_(Img.getSize()[0], 1500)
	eq_(Img.getSize()[1], 844)
	ok_( Img.isWide() )
	ok_( not Img.isSquare() )
	ok_( not Img.isDual() )

def WoImgFile_load_dual_test():
	file = '../3200x1080.jpg' #8:2.7
	Img = WoImgFile(file)
	eq_(Img.getSize()[0], 3200)
	eq_(Img.getSize()[1], 1080)
	ok_( Img.isDual() )
	ok_( not Img.isSquare() )
	ok_( not Img.isWide() )

def WoImgFile_load_no_match_test():
	file = '../1000x800.jpg'	#No Match
	Img = WoImgFile(file)
	eq_(Img.getSize()[0], 1000)
	eq_(Img.getSize()[1], 800)
	ok_( not Img.isSquare() )
	ok_( not Img.isWide() )
	ok_( not Img.isDual() )