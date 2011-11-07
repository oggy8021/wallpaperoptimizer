# -*- coding: utf-8 -*-

import sys
import os.path
import csv
import time
import logging

import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

#class Wo Dialog(object):

#		 Dialog = Wo Dialog(self.gladefile, self.logging)
#		 Dialog.openDialog( )

#	def btnOk_clicked(self, widget):
#		self.Dialog.response(gtk.RESPONSE_OK)

#	def btnCancel_clicked(self, widget):
#		self.Dialog.response(gtk.RESPONSE_CANCEL)

#	def openDialog(self, , ):
#		self.Dialog.show_all()
#pre
#		result = self.Dialog.run()
#		if (result == gtk.RESPONSE_OK):
#aft
#		self.Dialog.destroy()
#		return bgcolor

#	def __init__(self, gladefile, logger):
#		self.logging = logger
#		self.wTree = gtk.glade.XML(gladefile, " Dialog")
#		self.Dialog = self.wTree.get_widget(" Dialog")

#		dic = {
#			"on_btnOk_clicked" : self.btnOkColor_clicked,
#			"on_btnCancel_clicked" : self.btnCancel_clicked,
#			"on_ Dialog_destroy" : self.btnCancel_clicked
#			}
#		self.wTree.signal_autoconnect(dic)


class WoSettingDialog(object):

#	def btnOpenSrcdirL_clicked(self, widget):
#		SrcDirDialogL = WoSrcDirDialogL(self.gladefile, self.logging)
#		SrcDirDialogL.openDialog(self.srcdir[0])

#	def btnOpenSrcdirR_clicked(self, widget):
#		SrcDirDialogR = WoSrcDirDialogR(self.gladefile, self.logging)
#		SrcDirDialogR.openDialog(self.srcdir[1])

	def btnSaveSetting_clicked(self, widget):
#dummy
		configfile='~/Develop/WallPosit/trunk/.wallpositrc_gui'
		cf = csv.writer(file(os.path.expanduser(configfile), 'w'))
		cf.writerow([self.wTree.get_widget('entDisplayWL').get_text()
				 + 'x'
				 + self.wTree.get_widget('entDisplayHL').get_text()
				 , 'left'
				 , self.wTree.get_widget('entSrcdirL').get_text()
				 ])
		cf.writerow([self.wTree.get_widget('entDisplayWR').get_text()
				 + 'x'
				 + self.wTree.get_widget('entDisplayHR').get_text()
				 , 'right'
				 ,self.wTree.get_widget('entSrcdirR').get_text()
				 ])

	def btnClear_clicked(self, widget):
		self.wTree.get_widget('entDisplayWL').set_text('')
		self.wTree.get_widget('entDisplayHL').set_text('')
		self.wTree.get_widget('entDisplayWR').set_text('')
		self.wTree.get_widget('entDisplayHR').set_text('')
		self.wTree.get_widget('entSrcdirL').set_text('')
		self.wTree.get_widget('entSrcdirR').set_text('')

	def btnOk_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_OK)

	def btnCancel_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_CANCEL)

	def openDialog(self, displays, srcdirs):
		self.Dialog.show_all()
		disp = displays[0].split('x')
		self.wTree.get_widget('entDisplayWL').set_text(disp[0])
		self.wTree.get_widget('entDisplayHL').set_text(disp[1])
		disp = displays[1].split('x')
		self.wTree.get_widget('entDisplayWR').set_text(disp[0])
		self.wTree.get_widget('entDisplayHR').set_text(disp[1])
		self.wTree.get_widget('entSrcdirL').set_text(srcdirs[0])
		self.wTree.get_widget('entSrcdirR').set_text(srcdirs[1])
		result = self.Dialog.run()
		if (result == gtk.RESPONSE_OK):
			WoApplet.config['display'] = [
				self.wTree.get_widget('entDisplayWL').get_text()
				 + 'x' 
				 + self.wTree.get_widget('entDisplayHL').get_text()
				 ,
				self.wTree.get_widget('entDisplayWR').get_text()
				 + 'x' 
				 + self.wTree.get_widget('entDisplayHR').get_text()
				 ]
			WoApplet.config['srcdir'] = [
				self.wTree.get_widget('entSrcdirL').get_text()
				 ,
				self.wTree.get_widget('entSrcdirR').get_text()
				 ]
		self.Dialog.destroy()

	def __init__(self, gladefile, logger):
		self.logging = logger
		self.wTree = gtk.glade.XML(gladefile, "SettingDialog")
		self.Dialog = self.wTree.get_widget("SettingDialog")

		dic = {
#			"on_btnOpenSrcdirL_clicked" : self.btnOpenSrcdirL_clicked,
#			"on_btnOpenSrcdirR_clicked" : self.btnOpenSrcdirR_clicked,
			"on_btnClear_clicked" : self.btnClear_clicked,
			"on_btnSaveSetting_clicked" : self.btnSaveSetting_clicked,
			"on_btnOk_clicked" : self.btnOk_clicked,
			"on_btnCancel_clicked" : self.btnCancel_clicked,
			"on_SettingDialog_destroy" : self.btnCancel_clicked
			}
		self.wTree.signal_autoconnect(dic)


class WoColorSelectionDiag(object):

	def btnOk_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_OK)

	def btnCancel_clicked(self, widget):
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
# 直接、WoApplet.config書いてしまう手も？
		return bgcolor

	def __init__(self, gladefile, logger):
		self.logging = logger
		self.wTree = gtk.glade.XML(gladefile, "ColorSelectionDialog")
		self.Dialog = self.wTree.get_widget("ColorSelectionDialog")

		dic = {
			"on_btnOk_clicked" : self.btnOk_clicked,
			"on_btnCancel_clicked" : self.btnCancel_clicked,
			"on_ColorSelectionDialog_destroy" : self.btnCancel_clicked,
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

	def btnSetting_clicked(self, widget):
		SettingDialog = WoSettingDialog(self.gladefile, self.logging)
		SettingDialog.openDialog(WoApplet.config['display'], WoApplet.config['srcdir'])
#		print "set to display %s, %s" % (WoApplet.config['display'][0],WoApplet.config['display'][1])
#		print "set to srcdir %s, %s" % (WoApplet.config['srcdir'][0],WoApplet.config['srcdir'][1])

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

		#自クラスのconfigに、本体のconfigを放りこむ

		dic = {
			"on_tglBtn_pressed" : self.tglBtn_pressed,
			"on_tglBtn_toggled" : self.tglBtn_toggled,
			"on_tglBtn_released" : self.tglBtn_released,
			"on_entMergin_activate" : self.entMergin_activate,
			"on_radFixed_toggled" : self.radFixed_toggled,
			"on_btnSetting_clicked" : self.btnSetting_clicked,
			"on_btnSetColor_clicked" : self.btnSetColor_clicked,
#			"on_btnSave_clicked" : self.btnSave_clicked,
#			"on_btnSetWall_clicked" : self.btnSetWall_clicked,
			"on_entInterval_activate" : self.entInterval_activate,
#			"on_btnDaemonize_clicked" : self.btnDaemonize_clicked,
#			"on_btnCancelDamonize_clicked" : self.btnCancelDaemonize_clicked,
			"on_btnQuit_clicked" : gtk.main_quit,
#			"on_btn_clicked" : self.btn_clicked,
			"on_WallPosit_MainWindow_destroy" : gtk.main_quit
			}
		self.wTree.signal_autoconnect(dic)

	def finalize(self):
		gtk.main()
