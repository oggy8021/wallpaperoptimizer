# -*- coding: utf-8 -*-

#from WoBounds import WoBounds
from WoRectangle import WoRectangle

class WoWorkSpace(WoRectangle):

	def __init__(self):
		self.depth = 24

		WoRectangle.__init__(self)
		self.lScreen = WoRectangle()
		self.rScreen = WoRectangle()

		xdpyinfo='/usr/bin/xdpyinfo'
		import commands
		dimensions = commands.getoutput(xdpyinfo + '| grep dimensions')
		depth = commands.getoutput(xdpyinfo + '| grep "depth of root window"')

		import re
		#"  dimensions:    3200x1080 pixels (856x292 millimeters)"
		ptn = re.compile('[\s]+|x')
		subStr = ptn.split( dimensions )
		self.setSize(int(subStr[2]), int(subStr[3])) # WoRectangle Method

		ptn = re.compile('[\s]')
		subStr = ptn.split( depth )
		self.depth = int(subStr[9])

# lScreen, rScreenには作用していない

