# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_

from WallpaperOptimizer.WoConfig import WoConfig

def WoConfig_settigFile_test():
	wConfig = WoConfig('~/.wallpositrc')
	eq_(wConfig.lDisplay.getConfig()['width'], 1920)
	eq_(wConfig.lDisplay.getConfig()['height'], 1080)
	eq_(wConfig.lDisplay.getConfig()['posit'], 'left')
	eq_(wConfig.lDisplay.getConfig()['srcdir'], '~/Wallpaper(Sync)/3200/')

	eq_(wConfig.rDisplay.getConfig()['width'], 1280)
	eq_(wConfig.rDisplay.getConfig()['height'], 1024)
	eq_(wConfig.rDisplay.getConfig()['posit'], 'right')
	eq_(wConfig.rDisplay.getConfig()['srcdir'], '~/Wallpaper(Sync)/1280/')

	eq_(wConfig.lDisplay is wConfig.rDisplay, False)

	wConfig2 = WoConfig()
	eq_(wConfig2.lDisplay.getConfig()['height'], 1080)
	eq_(wConfig.lDisplay is wConfig2.lDisplay, False)

def WoConfig_settingArgs_test():
	wConfig = WoConfig('~/.wallpositrc', '1920x1080', '1280x1024', ['.','.'])
	eq_(wConfig.lDisplay.getConfig()['width'], 1920)
	eq_(wConfig.lDisplay.getConfig()['height'], 1080)
	eq_(wConfig.lDisplay.getConfig()['posit'], 'left')
	eq_(wConfig.lDisplay.getConfig()['srcdir'], '.')

	eq_(wConfig.rDisplay.getConfig()['width'], 1280)
	eq_(wConfig.rDisplay.getConfig()['height'], 1024)
	eq_(wConfig.rDisplay.getConfig()['posit'], 'right')
	eq_(wConfig.rDisplay.getConfig()['srcdir'], '.')

	eq_(wConfig.lDisplay is wConfig.rDisplay, False)

	wConfig2 = WoConfig()
	eq_(wConfig2.lDisplay.getConfig()['height'], 1080)
	eq_(wConfig.lDisplay is wConfig2.lDisplay, False)
