# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_

from WoConfig import WoConfig

def WoConfig_leftScreen_test():
	wConfig = WoConfig()
	eq_(wConfig.lScreen.getConfig()['width'], 1920)
	eq_(wConfig.lScreen.getConfig()['height'], 1080)
	eq_(wConfig.lScreen.getConfig()['posit'], 'left')
	eq_(wConfig.lScreen.getConfig()['depth'], 24)
	eq_(wConfig.lScreen.getConfig()['bgcolor'], 'black')

	eq_(wConfig.rScreen.getConfig()['width'], 1280)
	eq_(wConfig.rScreen.getConfig()['height'], 1024)
	eq_(wConfig.rScreen.getConfig()['posit'], 'right')
	eq_(wConfig.rScreen.getConfig()['depth'], 24)
	eq_(wConfig.rScreen.getConfig()['bgcolor'], 'black')

	eq_(wConfig.lScreen is wConfig.rScreen, False)
