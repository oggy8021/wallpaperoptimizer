# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_

from WoConfig import WoConfig

def WoConfig_leftDisplay_test():
	wConfig = WoConfig()
	eq_(wConfig.lDisplay.getConfig()['width'], 1920)
	eq_(wConfig.lDisplay.getConfig()['height'], 1080)
	eq_(wConfig.lDisplay.getConfig()['posit'], 'left')
	eq_(wConfig.lDisplay.getConfig()['depth'], 24)
	eq_(wConfig.lDisplay.getConfig()['bgcolor'], 'black')

	eq_(wConfig.rDisplay.getConfig()['width'], 1280)
	eq_(wConfig.rDisplay.getConfig()['height'], 1024)
	eq_(wConfig.rDisplay.getConfig()['posit'], 'right')
	eq_(wConfig.rDisplay.getConfig()['depth'], 24)
	eq_(wConfig.rDisplay.getConfig()['bgcolor'], 'black')

	eq_(wConfig.lDisplay is wConfig.rDisplay, False)

	wConfig2 = WoConfig()
	eq_(wConfig2.lDisplay.getConfig()['height'], 1080)
	eq_(wConfig.lDisplay is wConfig2.lDisplay, False)