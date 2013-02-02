# -*- coding: utf-8 -*-

import sys

try:
	import gtk.glade
except:
	print 'not installed GTK+ bindings: Glade support'
	print 'ex) sudo apt-get install python-glade2'
	print 'ex) sudo yum install pygtk2-libglade'
	sys.exit(2)

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

class Glade(gtk.glade.XML):

	def addPos(self, wName, label=False):
		retNode = self.get_widget(wName)
		pos = Position(wName, label)
		setattr(retNode, 'posit', pos)
		return retNode
