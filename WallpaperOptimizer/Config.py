# -*- coding: utf-8 -*-

# ~/wallpositrc
#1920x1080,left,srcdir
#1280x1024,right,srcdir

import os.path

class Config(object):

	class FormatError(Exception):
		def __init__(self, value):
			self.value = value
		def __str__(self):
			return repr(self.value)

	class Display(object):

		def getConfig(self):
			config = dict()
			config['width'] = self.width
			config['height'] = self.height
			config['posit'] = self.posit
			config['srcdir'] = self.srcdir
			return config

		def toIntAsSizeString(self, val):
			wh = val.split('x')
			self.width = int(wh[0])
			self.height = int(wh[1])

		def setWidth(self, val):
			self.width = val

		def setHeight(self, val):
			self.height = val

		def setPosit(self, val):
			self.posit = val

		def setSrcdir(self, val):
			self.srcdir = val

		def setConfig(self, w, h, p, s):
			self.width = w
			self.height = h
			self.posit = p
			self.srcdir = s

		def __init__(self):
			self.width = 0
			self.height = 0
			self.posit = None
			self.srcdir = ''

	def setConfig(self, size, p, s):
		if (p == 'left'):
			display = self.lDisplay
		elif (p == 'right'):
			display = self.rDisplay
		else:
			raise Config.FormatError("position setting is left or right")
		subStr = size.split('x')
		display.setConfig(int(subStr[0]), int(subStr[1]), p, s)

	def __init__(self
						, configfile=None
						, lsize=None
						, rsize=None
						, srcdir=['','']):
		self.lDisplay = Config.Display()
		self.rDisplay = Config.Display()

		if (configfile != None):
			# config set from configfile
			cf = open(os.path.expanduser(configfile), 'r')
			try:
				for i, cfline in enumerate(cf):
					subStr = cfline.rstrip().split(',')
					self.setConfig(subStr[0], subStr[1], subStr[2])

			except ValueError:
				cf.close()
				raise Config.FormatError("configfile written not expected Value")

			cf.close()
			if (i < 1):
				raise Config.FormatError("Config require 2 records")

		else:
			pass

# console版では、~/.wallpositrcは上書きしない
