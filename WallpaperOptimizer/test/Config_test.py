# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_

from WallpaperOptimizer.Config import Config

def Config_settigFile_test():
	wConfig = Config('~/.wallpositrc')
	eq_(wConfig.lDisplay.getConfig()['width'], 1920)
	eq_(wConfig.lDisplay.getConfig()['height'], 1080)
	eq_(wConfig.lDisplay.getConfig()['posit'], 'left')
	eq_(wConfig.lDisplay.getConfig()['srcdir'], '~/Wallpaper(Sync)/3200/')

	eq_(wConfig.rDisplay.getConfig()['width'], 1280)
	eq_(wConfig.rDisplay.getConfig()['height'], 1024)
	eq_(wConfig.rDisplay.getConfig()['posit'], 'right')
	eq_(wConfig.rDisplay.getConfig()['srcdir'], '~/Wallpaper(Sync)/1280/')

	eq_(wConfig.lDisplay is wConfig.rDisplay, False)


def Config_initialize_test():
	wConfig = Config()
	eq_(wConfig.lDisplay.getConfig()['width'], 0)
	eq_(wConfig.lDisplay.getConfig()['height'], 0)
	eq_(wConfig.lDisplay.getConfig()['posit'], None)
	eq_(wConfig.lDisplay.getConfig()['srcdir'], '')

	eq_(wConfig.rDisplay.getConfig()['width'], 0)
	eq_(wConfig.rDisplay.getConfig()['height'], 0)
	eq_(wConfig.rDisplay.getConfig()['posit'], None)
	eq_(wConfig.rDisplay.getConfig()['srcdir'], '')

	eq_(wConfig.lDisplay is wConfig.rDisplay, False)

def Config_writeConfig_test():
	wConfig = Config()
	wConfig.lDisplay.setSrcdir('/tmp')
	eq_(wConfig.lDisplay.getConfig()['srcdir'], '/tmp')

	wConfig.lDisplay.setSize('1920x1080')
	eq_(wConfig.lDisplay.getConfig()['width'], 1920)
	eq_(wConfig.lDisplay.getConfig()['height'], 1080)
