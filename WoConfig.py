# -*- coding: utf-8 -*-

class WoConfig(object):

	class WoScreenConfig(object):
		width = 0
		height = 0
		posit = None
		depth = 24
		bgcolor = 'black'

	#getter
		def getConfig(self):
			config['width'] = self.width
			config['height'] = self.height
			config['posit'] = self.posit
			config['depth'] = self.depth
			config['bgcolor'] = self.bgcolor
			return self.config

	#setter
		def setConfig(self, w, h, p, d, c):
			self.width = w
			self.height = h
			self.posit = p
			self.depth = d
			self.bgcolor = c

	lScreen = WoScreenConfig()
	rScreen = WoScreenConfig()

	def __init__(self):
		# .wallpositrc読む
		import sys
		import os.path
		configfile = '~/.wallpositrc'

		print os.path.expanduser(configfile)
