# -*- coding: utf-8 -*-

# ~/wallpositrc
#1920x1080,left,black
#1280x1024,right,black

class WoConfig(object):

	class WoDisplay(object):
		width = 0
		height = 0
		posit = None
		bgcolor = 'black'
		srcdir = '.'

		def getConfig(self):
			config = dict()
			config['width'] = self.width
			config['height'] = self.height
			config['posit'] = self.posit
			config['bgcolor'] = self.bgcolor
			config['srcdir'] = self.srcdir
			return config

		def setConfig(self, w, h, p, c, s):
			self.width = w
			self.height = h
			self.posit = p
			self.bgcolor = c
			self.srcdir = s

	def __init__(self
						, configfile='~/.wallpositrc'
						, lsize=None
						, rsize=None
						, bgcolor=None
						, srcdir='.'):
		self.lDisplay = WoConfig.WoDisplay()
		self.rDisplay = WoConfig.WoDisplay()

		import re
		ptn = re.compile(',|x')

		if (lsize == None and rsize == None):
			import sys
			import os.path

			cf = open(os.path.expanduser(configfile), 'r')
			for cfline in cf:
				subStr = ptn.split( cfline.rstrip() )
				if (bgcolor == None):
					bgcolor = subStr[3]
				if subStr[2] == 'left':
					self.lDisplay.setConfig(int(subStr[0])
											, int(subStr[1])
											, subStr[2]
											, bgcolor
											, subStr[4])
				else:
					self.rDisplay.setConfig(int(subStr[0])
											, int(subStr[1])
											, subStr[2]
											, bgcolor
											, subStr[4])
			cf.close()
		else:
			subStr = ptn.split( lsize )
			self.lDisplay.setConfig(int(subStr[0]), int(subStr[1]), 'left', bgcolor, srcdir)
			subStr = ptn.split( rsize )
			self.rDisplay.setConfig(int(subStr[0]), int(subStr[1]), 'right', bgcolor, srcdir)
			# ~/.wallpositrcは上書きしない

