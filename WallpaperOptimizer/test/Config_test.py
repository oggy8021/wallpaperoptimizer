# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_

from WallpaperOptimizer.Config import Config

def Config_settigFile_test():
	wConfig = Config('~/.walloptrc')
#	wConfig = Config('~/.walloptrc_')
	eq_(wConfig.lDisplay.getConfig()['width'], 1920)
	eq_(wConfig.lDisplay.getConfig()['height'], 1080)
	eq_(wConfig.lDisplay.getConfig()['posit'], 'left')
	eq_(wConfig.lDisplay.getConfig()['srcdir'], '~/Wallpaper(Sync)/1920/')

	eq_(wConfig.lDisplay.width, 1920)
	eq_(wConfig.lDisplay.height, 1080)
	eq_(wConfig.lDisplay.posit, 'left')
	eq_(wConfig.lDisplay.srcdir, '~/Wallpaper(Sync)/1920/')

	eq_(wConfig.rDisplay.getConfig()['width'], 1280)
	eq_(wConfig.rDisplay.getConfig()['height'], 1024)
	eq_(wConfig.rDisplay.getConfig()['posit'], 'right')
	eq_(wConfig.rDisplay.getConfig()['srcdir'], '~/Wallpaper(Sync)/1280/')

	eq_(wConfig.lDisplay is wConfig.rDisplay, False)
	eq_(wConfig.getBool(), True)


def Config_initialize_test():
	wConfig = Config()
	eq_(wConfig.lDisplay.getConfig()['width'], 0)
	eq_(wConfig.lDisplay.getConfig()['height'], 0)
	eq_(wConfig.lDisplay.getConfig()['posit'], 'left')
	eq_(wConfig.lDisplay.getConfig()['srcdir'], '')

	eq_(wConfig.rDisplay.getConfig()['width'], 0)
	eq_(wConfig.rDisplay.getConfig()['height'], 0)
	eq_(wConfig.rDisplay.getConfig()['posit'], 'right')
	eq_(wConfig.rDisplay.getConfig()['srcdir'], '')

	eq_(wConfig.lDisplay is wConfig.rDisplay, False)
	eq_(wConfig.getBool(), False)

def Config_writeConfig_test():
	wConfig = Config()
	wConfig.lDisplay.setSrcdir('/tmp')
	eq_(wConfig.lDisplay.getConfig()['srcdir'], '/tmp')

	wConfig.lDisplay.toIntAsSizeString('1920x1080')
	eq_(wConfig.lDisplay.getConfig()['width'], 1920)
	eq_(wConfig.lDisplay.getConfig()['height'], 1080)
