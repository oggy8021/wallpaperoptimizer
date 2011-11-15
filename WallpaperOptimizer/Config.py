# -*- coding: utf-8 -*-

# ~/wallpositrc
#1920x1080,left,srcdir
#1280x1024,right,srcdir

import os.path

class Config(object):

	class FormatError(Exception):
		def __init__(self, msg):
			self.value = msg
		def __str__(self):
			return repr(self.value)

	class Display(object):
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
						, srcdir=['','']):
		self.lDisplay = Config.Display()
		self.rDisplay = Config.Display()

		import re
		ptn = re.compile(',|x')

		if (lsize == None and rsize == None and srcdir[0] == '' and srcdir[1] == ''):
			# config set from configfile
			cf = open(os.path.expanduser(configfile), 'r')
			try:
				for i, cfline in enumerate(cf):
					subStr = ptn.split( cfline.rstrip() )
					if subStr[2] == 'left':
						self.lDisplay.setConfig(int(subStr[0])
												, int(subStr[1])
												, subStr[2]
												, subStr[3])
					elif subStr[2] == 'right':
						self.rDisplay.setConfig(int(subStr[0])
												, int(subStr[1])
												, subStr[2]
												, subStr[3])
					else:
						cf.close()
						raise Config.FormatError("position setting is left or right")
			except ValueError:
				cf.close()
				raise Config.FormatError("configfile written not expected Value")

			cf.close()
			if (i < 1):
				raise Config.FormatError("Config require 2 records")

		else:
			# config set from commandline option
			subStr = ptn.split( lsize )
			self.lDisplay.setConfig(int(subStr[0]), int(subStr[1]), 'left', srcdir[0])
			subStr = ptn.split( rsize )
			self.rDisplay.setConfig(int(subStr[0]), int(subStr[1]), 'right', srcdir[1])

# console版では、~/.wallpositrcは上書きしない
