# -*- coding: utf-8 -*-

import os.path
import time
import logging

import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

class WoApplet(object):

	mapdic = dict()
	mapdic['tglPushLeftL'] = 'tglPushRightL'
	mapdic['tglPushRightL'] = 'tglPushLeftL'
	mapdic['tglUpperL'] = 'tglLowerL'
	mapdic['tglLowerL'] = 'tglUpperL'
	mapdic['tglPushLeftR'] = 'tglPushRightR'
	mapdic['tglPushRightR'] = 'tglPushLeftR'
	mapdic['tglUpperR'] = 'tglLowerR'
	mapdic['tglLowerR'] = 'tglUpperR'

	config = dict()
	config['align'] = ['center','center']
	config['valign'] = ['middle','middle']
	config['mergin'] = [0,0,0,0]
	config['fixed'] = True
	config['display'] = ['1024x768','1024x768']
	config['bgcolor'] = 'black'
	config['srcdir'] = ['.','.']
	#左右独立、ワークスペース全体は未検討

	def tglBtn_pressed(self, widget):
		vsName = WoApplet.mapdic[widget.get_name()]
		if (self.wTree.get_widget(vsName).get_active()):
			self.wTree.get_widget(vsName).set_active(False)

	def tglBtn_toggled(self, widget):
		if (widget.get_active()):
			btnName = widget.get_name()
			attr = self.setConfigAttr(btnName)
			if (btnName.find('PushLeft') > 0):
				val = 'left'
			elif (btnName.find('PushRight') > 0):
				val = 'right'
			elif (btnName.find('Upper') > 0):
				val = 'top'
			elif (btnName.find('Lower') > 0):
				val = 'bottom'
			idx = self.setConfigIdx(btnName)
			WoApplet.config[attr][idx] = val
#			print "%s Enable set to %s [%s, %d]" % (btnName,WoApplet.config[attr][idx],attr,idx)

	def tglBtn_released(self, widget):
		vsName = WoApplet.mapdic[widget.get_name()]
		if (widget.get_active() == False and self.wTree.get_widget(vsName).get_active() == False):
			btnName = widget.get_name()
			attr = self.setConfigAttr(btnName)
			if (attr == 'align'):
				val = 'center'
			else:
				val = 'middle'
			idx = self.setConfigIdx(btnName)
			WoApplet.config[attr][idx] = val
#			print "%s Enable set to %s [%s, %d]" % (btnName,WoApplet.config[attr][idx],attr,idx)

	def setConfigAttr(self, btnName):
		if (btnName.find('PushLeft') > 0 or btnName.find('PushRight') > 0):
			attr = 'align'
		elif (btnName.find('Upper') > 0 or btnName.find('Lower') > 0):
			attr = 'valign'
		return attr

	def setConfigIdx(self, btnName):
		if (btnName.rfind('L') == (len(btnName) - 1)):
			idx = 0
		elif (btnName.rfind('R') == (len(btnName) - 1)):
			idx = 1
		return idx

	def finalize(self):
		gtk.main()

	def __init__(self, logger):
		self.logging = logger
		self.gladefile = os.path.abspath("./WallpaperOptimizer/glade/wallpositapplet.glade")
		self.wTree = gtk.glade.XML(self.gladefile)
		self.window = self.wTree.get_widget("WallPosit_MainWindow")

		dic = {
			"on_tglBtn_pressed" : self.tglBtn_pressed,
			"on_tglBtn_toggled" : self.tglBtn_toggled,
			"on_tglBtn_released" : self.tglBtn_released,
			"on_WallPosit_MainWindow_destroy" : gtk.main_quit,
			"on_btnQuit_clicked" : gtk.main_quit
			}
		self.wTree.signal_autoconnect(dic)


