# -*- coding: utf-8 -*-

# ~/wallpositrc
#1920x1080,left,24,black
#1280x1024,right,24,black

class WoConfig(object):

	class WoDisplay(object):
		width = 0
		height = 0
		posit = None
		depth = 24
		bgcolor = 'black'

	#getter
		def getConfig(self):
			config = dict()
			config['width'] = self.width
			config['height'] = self.height
			config['posit'] = self.posit
			config['depth'] = self.depth
			config['bgcolor'] = self.bgcolor
			return config

	#setter
		def setConfig(self, w, h, p, d, c):
			self.width = w
			self.height = h
			self.posit = p
			self.depth = d
			self.bgcolor = c

	def __init__(self):
		self.lDisplay = WoConfig.WoDisplay()
		self.rDisplay = WoConfig.WoDisplay()

		import sys
		import os.path
		import re
		ptn = re.compile(',|x')

		configfile = '~/.wallpositrc'
		cf = open(os.path.expanduser(configfile), 'r')
		for cfline in cf:
			subStr = ptn.split( cfline.rstrip() )
			if subStr[2] == 'left':
				self.lDisplay.setConfig(int(subStr[0]), int(subStr[1]), subStr[2], int(subStr[3]), subStr[4])
			else:
				self.rDisplay.setConfig(int(subStr[0]), int(subStr[1]), subStr[2], int(subStr[3]), subStr[4])
		cf.close()
