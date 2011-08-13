# -*- coding: utf-8 -*-

from PIL import Image
from WoRectangle import WoRectangle

class WoImgFile(WoRectangle, Image.Image):

	def __init__(self,file=''):
		WoRectangle.__init__(self)
		if (file == ''):
			mode = 'RGB'
			size = (5, 5)
			self._img = Image.new(mode, size)
		else:
			self._img = Image.open(file)
		self.setSize(self._img.size[0], self._img.size[1])

	def show(self):
		self._img.show()

	def reSize(self, w, h):
		size = (w, h)
		self._img = self._img.resize(size)
		self.setSize(self._img.size[0], self._img.size[1])

if __name__ == "__main__":
	pass
