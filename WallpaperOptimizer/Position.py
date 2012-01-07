# -*- coding: utf-8 -*-

class Position(object):

	def __init__(self, tag, label=False):
		if tag.rfind('L') == (len(tag) - 1):
			self.idx = 0
			self.Caps = 'L'
			if label:
				self.Kanji = '左'
		elif tag.rfind('R') == (len(tag) - 1):
			self.idx = 1
			self.Caps = 'R'
			if label:
				self.Kanji = '右'
