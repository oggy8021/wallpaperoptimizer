# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_

from WoWorkSpace import WoWorkSpace

def WoWorkSpace_init_test():
	ws = WoWorkSpace()
	eq_(ws.Size.w, 3200)
	eq_(ws.Size.h, 1080)
