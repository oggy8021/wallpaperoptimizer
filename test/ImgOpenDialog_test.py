# -*- coding: utf-8 -*-

import os.path
import WallpaperOptimizer

from WallpaperOptimizer.Widget.ImgOpenDialog import ImgOpenDialog

from nose.tools import ok_, eq_

def ImgfileOpenSetNullPath_test():
	gladefile = os.path.abspath(os.path.join(WallpaperOptimizer.LIBRARYDIR,'glade','wallpositapplet.glade'))
	path = ''
	addlr = u'左'

	imgDialog = ImgOpenDialog(gladefile)
	path = imgDialog.openDialog(path, addlr)
	assert(path != '')

def ImgfileOpenSetPath_test():
	gladefile = os.path.abspath(os.path.join(WallpaperOptimizer.LIBRARYDIR,'glade','wallpositapplet.glade'))
	path1 = '/home/katsu/Develop/WallPosit.git/1000x800.jpg'
	addlr = u'右'

	imgDialog = ImgOpenDialog(gladefile)
	path2 = imgDialog.openDialog(path1, addlr)
	eq_(path2, path1)

if __name__ == "__main__":
	ImgfileOpenSetNullPath_test()
	ImgfileOpenSetPath_test()