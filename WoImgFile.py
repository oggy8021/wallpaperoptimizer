# -*- coding: utf-8 -*-

from PIL import Image
from WoRectangle import WoRectangle

class WoImgFile(WoRectangle, Image.Image):

	def __init__(self,file='', w=5, h=5, color='black'):
		WoRectangle.__init__(self)
		if (file == ''):
			mode = 'RGB'
			size = (w, h)
			self._img = Image.new(mode, size, color)
		else:
			self._img = Image.open(file)
		self.setSize(self._img.size[0], self._img.size[1])

	def show(self):
		self._img.show()

	def reSize(self, w, h):
		size = (w, h)
		self._img = self._img.resize(size)
		self.setSize(self._img.size[0], self._img.size[1])

	def paste(self, image, box):
		self._img.paste(image._img, box)
