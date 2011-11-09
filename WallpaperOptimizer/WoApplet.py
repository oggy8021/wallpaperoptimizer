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

from WallpaperOptimizer.WoCore import WoCore


class WoAppletUtil(object):
	@staticmethod
	def judgeLeftRight(wName):
		if (wName.rfind('L') == (len(wName) - 1)):
			idx = 0
		elif (wName.rfind('R') == (len(wName) - 1)):
			idx = 1
		return idx


class WoImgOpenDialog(object):

	def btnOpen_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_OK)

	def btnCancel_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_CANCEL)

	def openDialog(self):
		self.Dialog.show_all()
		result = self.Dialog.run()
		if (result == gtk.RESPONSE_OK):
			imgfile = self.Dialog.get_filename()
			self.Dialog.destroy()
			return imgfile
		else:
			self.Dialog.destroy()
			return ''

	def __init__(self, gladefile, logger):
		self.logging = logger
		self.wTree = gtk.glade.XML(gladefile, "ImgOpenDialog")
		self.Dialog = self.wTree.get_widget("ImgOpenDialog")
		imgFilter = gtk.FileFilter()
		imgFilter.set_name("画像")
# WoChanger的には、この４つ
		imgFilter.add_mime_type("image/png")
		imgFilter.add_mime_type("image/jpeg")
		imgFilter.add_mime_type("image/bmp")
		imgFilter.add_mime_type("image/gif")
		imgFilter.add_pattern("*.png")
		imgFilter.add_pattern("*.jpeg")
		imgFilter.add_pattern("*.jpg")
		imgFilter.add_pattern("*.bmp")
		imgFilter.add_pattern("*.gif")
		self.Dialog.add_filter(imgFilter)
		allFile = gtk.FileFilter()
		allFile.set_name("全て")
		allFile.add_pattern("*")
		self.Dialog.add_filter(allFile)

		dic = {
			"on_btnOpen_clicked" : self.btnOpen_clicked,
			"on_btnCancel_clicked" : self.btnCancel_clicked,
			"on_ImgOpenDialog_destroy" : self.btnCancel_clicked
			}
		self.wTree.signal_autoconnect(dic)


class WoSrcdirDialog(object):

	def btnOpen_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_OK)

	def btnCancel_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_CANCEL)
#キャンセルでも設定が残る

	def openDialog(self, srcdir):
		self.Dialog.show_all()
		result = self.Dialog.run()
		if (result == gtk.RESPONSE_OK):
			srcdir = self.Dialog.get_current_folder()
		self.Dialog.destroy()
		return srcdir

	def __init__(self, gladefile, logger):
		self.logging = logger
		self.wTree = gtk.glade.XML(gladefile, "SrcDirDialog")
		self.Dialog = self.wTree.get_widget("SrcDirDialog")

		dic = {
			"on_btnOpen_clicked" : self.btnOpen_clicked,
			"on_btnCancel_clicked" : self.btnCancel_clicked,
			"on_SrcdirDialog_destroy" : self.btnCancel_clicked
			}
		self.wTree.signal_autoconnect(dic)


class WoSettingDialog(object):

	def btnOpenSrcdir_clicked(self, widget):
		wName = widget.get_name()
		lr = WoAppletUtil.judgeLeftRight(wName)
		SrcDirDialog = WoSrcdirDialog(self.gladefile, self.logging)
		self.srcdirs[lr] = SrcDirDialog.openDialog(self.srcdirs[lr])
		if (lr == 0):
			self.wTree.get_widget('entSrcdirL').set_text(self.srcdirs[lr])
		else:
			self.wTree.get_widget('entSrcdirR').set_text(self.srcdirs[lr])

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
		self.srcdirs = srcdirs

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
		self.gladefile = gladefile
		self.logging = logger
		self.wTree = gtk.glade.XML(gladefile, "SettingDialog")
		self.Dialog = self.wTree.get_widget("SettingDialog")

		dic = {
			"on_btnOpenSrcdir_clicked" : self.btnOpenSrcdir_clicked,
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
#TODO:直接、WoApplet.config書いてしまう手も？
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


class WoSaveWallpaperDialog(object):

	def btnOpen_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_OK)

	def btnCancel_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_CANCEL)

	def openDialog(self, Option, Config, Ws, images):
		self.Dialog.show_all()
		result = self.Dialog.run()
		if (result == gtk.RESPONSE_OK):
#TODO:ホントは値あるなしなど、チェックがいる
			Option.args[0] = images[0]
			Option.args[1] = images[1]
			Option.opts.save = self.Dialog.get_filename()
			Core = WoCore(WoApplet.logging)
			Core.singlerun(Option, Config, Ws)
		self.Dialog.destroy()

	def __init__(self, gladefile, logger):
		self.gladefile = gladefile
		self.logging = logger
		self.wTree = gtk.glade.XML(gladefile, "SaveWallpaperDialog")
		self.Dialog = self.wTree.get_widget("SaveWallpaperDialog")

		dic = {
			"on_btnOpen_clicked" : self.btnOpen_clicked,
			"on_btnCancel_clicked" : self.btnCancel_clicked,
			"on_SaveWallpaperDialog_destroy" : self.btnCancel_clicked
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
	#TODO:str,int行ったり来たり
	config['display'] = ['1024x768','1024x768']
	config['bgcolor'] = 'black'
	config['srcdir'] = ['.','.']
	#TODO:左右独立、ワークスペース全体は未検討

	option = dict()
	option['interval'] = 60

	def setConfigAttr(self, btnName):
		if (btnName.find('PushLeft') > 0 or btnName.find('PushRight') > 0):
			attr = 'align'
		elif (btnName.find('Upper') > 0 or btnName.find('Lower') > 0):
			attr = 'valign'
		return attr

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
			lr = WoAppletUtil.judgeLeftRight(wName)
			WoApplet.config[attr][lr] = val

	def tglBtn_released(self, widget):
		vsName = WoApplet.mapdic[widget.get_name()]
		if (widget.get_active() == False and self.wTree.get_widget(vsName).get_active() == False):
			wName = widget.get_name()
			attr = self.setConfigAttr(wName)
			if (attr == 'align'):
				val = 'center'
			elif (attr == 'valign'):
				val = 'middle'
			lr = WoAppletUtil.judgeLeftRight(wName)
			WoApplet.config[attr][lr] = val

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

	def btnGetImg_clicked(self, widget):
		wName = widget.get_name()
		lr = WoAppletUtil.judgeLeftRight(wName)
		ImgOpenDialog = WoImgOpenDialog(self.gladefile, self.logging)
		self.images[lr] = ImgOpenDialog.openDialog()
		if (lr == 0):
			self.wTree.get_widget('entPathL').set_text(self.images[lr])
		else:
			self.wTree.get_widget('entPathR').set_text(self.images[lr])

	def entImgPath_activate(self, widget):
		wName = widget.get_name()
		lr = WoAppletUtil.judgeLeftRight(wName)
		self.images[lr] = os.path.expanduser(self.wTree.get_widget(wName).get_text())
		if (lr == 0):
			self.wTree.get_widget('entPathL').set_text(self.images[lr])
		else:
			self.wTree.get_widget('entPathR').set_text(self.images[lr])
#TODO: 拡張子チェック?

	def btnSetting_clicked(self, widget):
		SettingDialog = WoSettingDialog(self.gladefile, self.logging)
		SettingDialog.openDialog(WoApplet.config['display'], WoApplet.config['srcdir'])

	def btnSetColor_clicked(self, widget):
		ColorSelectionDialog = WoColorSelectionDiag(self.gladefile ,self.logging)
		WoApplet.config['bgcolor'] = ColorSelectionDialog.openDialog(WoApplet.config['bgcolor'])

	def btnSave_clicked(self, widget):
		 SaveWallpaperDialog = WoSaveWallpaperDialog(self.gladefile, self.logging)
		 SaveWallpaperDialog.openDialog(self.Option, self.Config, self.Ws, self.images)

	def btnSetWall_clicked(self, widget):
		self.Option.args[0] = self.images[0]
		self.Option.args[1] = self.images[1]
		self.Option.opts.setWall = True
		Core = WoCore(self.logging)
		Core.singlerun(self.Option, self.Config, self.Ws)

	def entInterval_activate(self, widget):
		wName = widget.get_name()
		WoApplet.option['interval'] = int(self.wTree.get_widget(wName).get_text())

	def btnDaemonize_clicked(self, widget):
		WidthHeight = WoApplet.config['display'][0].split('x')
		self.Config.lDisplay.setConfig(int(WidthHeight[0]),
										int(WidthHeight[1]),
										self.Config.lDisplay.getConfig()['posit'],
										WoApplet.config['srcdir'][0])
		WidthHeight = WoApplet.config['display'][1].split('x')
		self.Config.rDisplay.setConfig(int(WidthHeight[0]),
										int(WidthHeight[1]),
										self.Config.rDisplay.getConfig()['posit'],
										WoApplet.config['srcdir'][1])
		self.Option.opts.interval = WoApplet.option['interval']
		Core = WoCore(self.logging)
		Core.daemonize(self.Option, self.Config, self.Ws)

#	def btnCancelDaemonize_clicked(self, widget):
#		raise CancelDaemonizeException

	def __init__(self, Option, Config, Ws, logger):
		self.Option = Option
		self.Option.args = ['','']
		self.Config = Config
		self.Ws = Ws
		self.logging = logger
		self.images = ['','']

		WoApplet.config['display'] = [
			str(self.Config.lDisplay.getConfig()['width']) +
			 'x' +
			  str(self.Config.lDisplay.getConfig()['height']),
			str(self.Config.rDisplay.getConfig()['width']) +
			 'x' +
			  str(self.Config.rDisplay.getConfig()['height']),
			]
		WoApplet.config['srcdir'] = [
			self.Config.lDisplay.getConfig()['srcdir'],
			self.Config.rDisplay.getConfig()['srcdir']
			]

		self.gladefile = os.path.abspath("./WallpaperOptimizer/glade/wallpositapplet.glade")
		self.wTree = gtk.glade.XML(self.gladefile, "WallPosit_MainWindow")
		self.window = self.wTree.get_widget("WallPosit_MainWindow")

		dic = {
			"on_tglBtn_pressed" : self.tglBtn_pressed,
			"on_tglBtn_toggled" : self.tglBtn_toggled,
			"on_tglBtn_released" : self.tglBtn_released,
			"on_entMergin_activate" : self.entMergin_activate,
			"on_radFixed_toggled" : self.radFixed_toggled,
			"on_btnGetImg_clicked" : self.btnGetImg_clicked,
			"on_entPath_activate" : self.entImgPath_activate,
			"on_btnSetting_clicked" : self.btnSetting_clicked,
			"on_btnSetColor_clicked" : self.btnSetColor_clicked,
			"on_btnSave_clicked" : self.btnSave_clicked,
			"on_btnSetWall_clicked" : self.btnSetWall_clicked,
			"on_entInterval_activate" : self.entInterval_activate,
			"on_btnDaemonize_clicked" : self.btnDaemonize_clicked,
#			"on_btnCancelDamonize_clicked" : self.btnCancelDaemonize_clicked,
			"on_btnQuit_clicked" : gtk.main_quit,
			"on_WallPosit_MainWindow_destroy" : gtk.main_quit
			}
		self.wTree.signal_autoconnect(dic)

	def finalize(self):
		gtk.main()
