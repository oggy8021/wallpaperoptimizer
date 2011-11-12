# -*- coding: utf-8 -*-

from WallpaperOptimizer.Imaging.Rectangle import Rectangle

class WorkSpace(Rectangle):

	def setScreenSize(self, lDisplay, rDisplay):
		self.lScreen.setSize(lDisplay[0], lDisplay[1])
		self.rScreen.setSize(rDisplay[0], rDisplay[1])

	def getScreenSize(self):
		return [[self.lScreen.Size.w, self.lScreen.Size.h]
			, [self.rScreen.Size.w, self.rScreen.Size.h]]

	def getDepth(self):
		return self.depth

	def compareToScreen(self):
		if ( self.Size.w < (self.lScreen.Size.w + self.rScreen.Size.w) ):
			return False
		if ( self.Size.h > self.lScreen.Size.h ):
			setattr(self.lScreen.Size, 'islessThanWorkSpaceHeight', True)
		elif ( self.Size.h > self.rScreen.Size.h ):
			setattr(self.rScreen.Size, 'islessThanWorkSpaceHeight', True)
		else:
			pass
		return True

	def setScreenType(self):
		if ( self.lScreen.isSquare() ):
			setattr(self.lScreen, 'displayType', 'square')
		if ( self.lScreen.isWide() ):
			setattr(self.lScreen, 'displayType', 'wide')

		if ( self.rScreen.isSquare() ):
			setattr(self.rScreen, 'displayType', 'square')
		if ( self.rScreen.isWide() ):
			setattr(self.rScreen, 'displayType', 'wide')

	def __init__(self):
		self.depth = 24

		Rectangle.__init__(self)
		self.lScreen = Rectangle()
		self.rScreen = Rectangle()

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

