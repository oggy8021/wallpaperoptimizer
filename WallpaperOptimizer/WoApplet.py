# -*- coding: utf-8 -*-

import os.path
import time
import logging

import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

class WoColorSelectionDiag(object):

	def btnOkColor_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_OK)

	def btnCancelColor_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_CANCEL)

	def openDialog(self, bgcolor):
		self.Dialog.show_all()
		gdkColor = gtk.gdk.Color()
		gdkColor = gtk.color_selection_palette_from_string(bgcolor)
		self.wTree.get_widget('color_selection').set_current_color(gdkColor[0])
		result = self.Dialog.run()
		if (result == gtk.RESPONSE_OK):
			gtkColor = self.wTree.get_widget('color_selection').get_current_color()
			bgcolor = gtk.color_selection_palette_to_string([gtkColor])
		self.Dialog.destroy()
		return bgcolor

	def __init__(self, gladefile, logger):
		self.logging = logger
		self.wTree = gtk.glade.XML(gladefile, "ColorSelectionDialog")
		self.Dialog = self.wTree.get_widget("ColorSelectionDialog")

		dic = {
			"on_btnOkColor_clicked" : self.btnOkColor_clicked,
			"on_ColorSelectionDialog_destroy" : self.btnCancelColor_clicked,
			"on_btnCancelColor_clicked" : self.btnCancelColor_clicked
			}
		self.wTree.signal_autoconnect(dic)


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

	option = dict()
	option['interval'] = 60

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

	def tglBtn_pressed(self, widget):
		vsName = WoApplet.mapdic[widget.get_name()]
		if (self.wTree.get_widget(vsName).get_active()):
			self.wTree.get_widget(vsName).set_active(False)

	def tglBtn_toggled(self, widget):
		if (widget.get_active()):
			wName = widget.get_name()
			attr = self.setConfigAttr(wName)
			if (wName.find('PushLeft') > 0):
				val = 'left'
			elif (wName.find('PushRight') > 0):
				val = 'right'
			elif (wName.find('Upper') > 0):
				val = 'top'
			elif (wName.find('Lower') > 0):
				val = 'bottom'
			idx = self.setConfigIdx(wName)
			WoApplet.config[attr][idx] = val

	def tglBtn_released(self, widget):
		vsName = WoApplet.mapdic[widget.get_name()]
		if (widget.get_active() == False and self.wTree.get_widget(vsName).get_active() == False):
			wName = widget.get_name()
			attr = self.setConfigAttr(wName)
			if (attr == 'align'):
				val = 'center'
			elif (attr == 'valign'):
				val = 'middle'
			idx = self.setConfigIdx(wName)
			WoApplet.config[attr][idx] = val

	def entMergin_activate(self, widget):
		wName = widget.get_name()
		if (wName.find('LMergin')) > 0:
			idx = 0
		elif (wName.find('RMergin')) > 0:
			idx = 1
		elif (wName.find('TopMergin')) > 0:
			idx = 2
		elif (wName.find('BtmMergin')) > 0:
			idx = 3
		WoApplet.config['mergin'][idx] = int(self.wTree.get_widget(wName).get_text())

	def radFixed_toggled(self, widget):
		wName = widget.get_name()
		WoApplet.config['fixed'] = self.wTree.get_widget(wName).get_active()

	def btnSetColor_clicked(self, widget):
		ColorSelectionDialog = WoColorSelectionDiag(self.gladefile ,self.logging)
		WoApplet.config['bgcolor'] = ColorSelectionDialog.openDialog(WoApplet.config['bgcolor'])
#		print "set to bgcolor %s" % WoApplet.config['bgcolor']

	def entInterval_activate(self, widget):
		wName = widget.get_name()
		WoApplet.option['interval'] = int(self.wTree.get_widget(wName).get_text())


	def __init__(self, logger):
		self.logging = logger
		self.gladefile = os.path.abspath("./WallpaperOptimizer/glade/wallpositapplet.glade")
		self.wTree = gtk.glade.XML(self.gladefile, "WallPosit_MainWindow")
		self.window = self.wTree.get_widget("WallPosit_MainWindow")

		dic = {
			"on_tglBtn_pressed" : self.tglBtn_pressed,
			"on_tglBtn_toggled" : self.tglBtn_toggled,
			"on_tglBtn_released" : self.tglBtn_released,
			"on_entMergin_activate" : self.entMergin_activate,
			"on_radFixed_toggled" : self.radFixed_toggled,
			"on_btnSetColor_clicked" : self.btnSetColor_clicked,
			"on_entInterval_activate" : self.entInterval_activate,
			"on_WallPosit_MainWindow_destroy" : gtk.main_quit,
			"on_btnQuit_clicked" : gtk.main_quit
			}
		self.wTree.signal_autoconnect(dic)

	def finalize(self):
		gtk.main()
