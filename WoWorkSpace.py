#!/usr/bin/env python

# -*- coding: utf-8 -*-

from WoBounds import WoBounds
from WoRectangle import WoRectangle

class WoWorkSpace(WoRectangle):

	Screen1 = WoBounds()
	Screen2 = WoBounds()

	def __init__(self):
		xdpyinfo='/usr/bin/xdpyinfo'

		import commands
		retval = commands.getoutput(xdpyinfo + '| grep dimensions')

		import re
		#"  dimensions:    3200x1080 pixels (856x292 millimeters)"
		ptn = re.compile('[\s]+|x')
		subStr = ptn.split( retval )
		self.setSize(int(subStr[2]), int(subStr[3])) # WoRectangle Method
