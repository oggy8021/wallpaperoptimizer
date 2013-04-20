# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_

from WallpaperOptimizer.Config import Config

def Config_settigFile_test():
	wConfig = Config('/home/katsu/.local/share/wallpaperoptimizer/.walloptrc')
#	wConfig = Config('~/.walloptrc_')
	eq_(wConfig.lDisplay.width, 1920)
	eq_(wConfig.lDisplay.height, 1080)
	eq_(wConfig.lDisplay.posit, 'left')
	eq_(wConfig.lDisplay.srcdir, '/home/katsu/Wallpaper/1920')

	eq_(wConfig.rDisplay.width, 1280)
	eq_(wConfig.rDisplay.height, 1024)
	eq_(wConfig.rDisplay.posit, 'right')
	eq_(wConfig.rDisplay.srcdir, '/home/katsu/Wallpaper/1280')

	eq_(wConfig.lDisplay is wConfig.rDisplay, False)
	eq_(wConfig.lDisplay.getBool(), True)
	eq_(wConfig.rDisplay.getBool(), True)


def Config_initialize_test():
	wConfig = Config()
	eq_(wConfig.lDisplay.width, 0)
	eq_(wConfig.lDisplay.height, 0)
	eq_(wConfig.lDisplay.posit, 'left')
	eq_(wConfig.lDisplay.srcdir, '')

	eq_(wConfig.rDisplay.width, 0)
	eq_(wConfig.rDisplay.height, 0)
	eq_(wConfig.rDisplay.posit, 'right')
	eq_(wConfig.rDisplay.srcdir, '')

	eq_(wConfig.lDisplay is wConfig.rDisplay, False)
	eq_(wConfig.lDisplay.getBool(), False)
	eq_(wConfig.rDisplay.getBool(), False)

def Config_writeConfig_test():
	wConfig = Config()
	wConfig.lDisplay.setSrcdir('/tmp')
	eq_(wConfig.lDisplay.srcdir, '/tmp')

	wConfig.lDisplay.toIntAsSizestring('1920x1080')
	eq_(wConfig.lDisplay.width, 1920)
	eq_(wConfig.lDisplay.height, 1080)
