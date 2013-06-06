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

	def __init__(self, idx, label=False):
		if idx == 0:
			self.idx = idx
			self.Caps = 'L'
			if label:
				self.Kanji = u'左'
		elif idx == 1:
			self.idx = idx
			self.Caps = 'R'
			if label:
				self.Kanji = u'右'

class Glade(gtk.glade.XML):

	def addPos(self, wName, label=False):
		retNode = self.get_widget(wName)
		if (wName.endswith('L')):
			pos = Position(0, label)
		elif(wName.endswith('R')):
			pos = Position(1, label)
		else:
			return retNode
		setattr(retNode, 'posit', pos)
		return retNode