#!/usr/bin/env python

# -*- coding: utf-8 -*-

from PIL import Image
from WoRectangle import WoRectangle

class WoImgFile(WoRectangle, Image.Image):

	def __init__(self,file=''):
		if (file is ''):
			mode = 'RGB'
			size = (5, 5)
			self._img = Image.new(mode, size)
		else:
			self._img = Image.open(file)
		self.setSize(self._img.size[0], self._img.size[1])
