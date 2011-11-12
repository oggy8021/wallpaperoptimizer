# -*- coding: utf-8 -*-

# ~/wallpositrc
#1920x1080,left,srcdir
#1280x1024,right,srcdir

import sys
import os.path

class WoConfig(object):

	class WoDisplay(object):
		width = 0
		height = 0
		posit = None
		srcdir = '.'

		def getConfig(self):
			config = dict()
			config['width'] = self.width
			config['height'] = self.height
			config['posit'] = self.posit
			config['srcdir'] = self.srcdir
			return config

		def setConfig(self, w, h, p, s):
			self.width = w
			self.height = h
			self.posit = p
			self.srcdir = s

	def __init__(self
						, configfile='~/.wallpositrc'
						, lsize=None
						, rsize=None
						, srcdir=['.','.']):
		self.lDisplay = WoConfig.WoDisplay()
		self.rDisplay = WoConfig.WoDisplay()

		import re
		ptn = re.compile(',|x')

		if (lsize == None and rsize == None):
			cf = open(os.path.expanduser(configfile), 'r')
			for cfline in cf:
				subStr = ptn.split( cfline.rstrip() )
				if subStr[2] == 'left':
					self.lDisplay.setConfig(int(subStr[0])
											, int(subStr[1])
											, subStr[2]
											, subStr[3])
				else:
					self.rDisplay.setConfig(int(subStr[0])
											, int(subStr[1])
											, subStr[2]
											, subStr[3])
			cf.close()
		else:
			subStr = ptn.split( lsize )
			self.lDisplay.setConfig(int(subStr[0]), int(subStr[1]), 'left', srcdir[0])
			subStr = ptn.split( rsize )
			self.rDisplay.setConfig(int(subStr[0]), int(subStr[1]), 'right', srcdir[1])
			# ~/.wallpositrcは上書きしない

