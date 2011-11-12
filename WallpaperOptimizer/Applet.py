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
import gobject

from WallpaperOptimizer.Core import Core


class AppletUtil(object):
	@staticmethod
	def judgeLeftRight(wName):
		if (wName.rfind('L') == (len(wName) - 1)):
			idx = 0
		elif (wName.rfind('R') == (len(wName) - 1)):
			idx = 1
		return idx

	@staticmethod
	def setAppletConfig(Option, Config, Ws):
		Applet.config['display'] = [
			str(Config.lDisplay.getConfig()['width']) +
			 'x' +
			  str(Config.lDisplay.getConfig()['height']),
			str(Config.rDisplay.getConfig()['width']) +
			 'x' +
			  str(Config.rDisplay.getConfig()['height']),
			]
		Applet.config['srcdir'] = [
			Config.lDisplay.getConfig()['srcdir'],
			Config.rDisplay.getConfig()['srcdir']
			]
		Applet.config['interval'] = Option.opts.interval

	@staticmethod
	def getSettingDialog(lr):
		if (lr == 0):
			lr = 'L'
		else:
			lr = 'R'
		return [self.wTree.get_widget('entDisplayW' + lr).get_text()
				 + 'x'
				 + self.wTree.get_widget('entDisplayH' + lr).get_text()
				 , 'left'
				 , self.wTree.get_widget('entSrcdir' + lr).get_text()
				 ]

	@staticmethod
	def setCoreArg(Option, Config, Ws):
		Option.opts.align = Applet.config['align']
		Option.opts.valign = Applet.config['valign']
		Option.opts.mergin = Applet.config['mergin']
		Option.opts.fixed = Applet.config['fixed']
		Option.opts.bgcolor = Applet.config['bgcolor']
		Option.opts.interval = Applet.option['interval']

		WidthHeight = Applet.config['display'][0].split('x')
		config.lDisplay.setConfig(int(WidthHeight[0]),
										int(WidthHeight[1]),
										config.lDisplay.getConfig()['posit'],
										Applet.config['srcdir'][0])
		WidthHeight = Applet.config['display'][1].split('x')
		config.rDisplay.setConfig(int(WidthHeight[0]),
										int(WidthHeight[1]),
										config.rDisplay.getConfig()['posit'],
										Applet.config['srcdir'][1])

#		Wsセットしていない

class ImgOpenDialog(object):

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
# Changer的には、この４つ
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


class SrcdirDialog(object):

	def btnOpen_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_OK)

	def btnCancel_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_CANCEL)

	def openDialog(self, srcdir):
		self.Dialog.show_all()
		result = self.Dialog.run()
		if (result == gtk.RESPONSE_OK):
			srcdir = self.Dialog.get_current_folder()
			self.Dialog.destroy()
			return srcdir
		else:
			self.Dialog.destroy()

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


class SettingDialog(object):

	def btnOpenSrcdir_clicked(self, widget):
		wName = widget.get_name()
		lr = AppletUtil.judgeLeftRight(wName)
		SrcDirDialog = SrcdirDialog(self.gladefile, self.logging)
		self.srcdirs[lr] = SrcDirDialog.openDialog(self.srcdirs[lr])
		if (lr == 0):
			self.wTree.get_widget('entSrcdirL').set_text(self.srcdirs[lr])
		else:
			self.wTree.get_widget('entSrcdirR').set_text(self.srcdirs[lr])

	def btnSaveSetting_clicked(self, widget):
#dummy
		configfile='~/Develop/WallPosit/trunk/.wallpositrc_gui'
		cf = csv.writer(file(os.path.expanduser(configfile), 'w'))
		cf.writerow(AppletUtil.getSettingDialog(0))
		cf.writerow(AppletUtil.getSettingDialog(1))

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
			Applet.config['display'] = [
				self.wTree.get_widget('entDisplayWL').get_text()
				 + 'x' 
				 + self.wTree.get_widget('entDisplayHL').get_text()
				 ,
				self.wTree.get_widget('entDisplayWR').get_text()
				 + 'x' 
				 + self.wTree.get_widget('entDisplayHR').get_text()
				 ]
			Applet.config['srcdir'] = [
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


class ColorSelectionDiag(object):

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
		Applet.config['bgcolor'] = bgcolor

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


class SaveWallpaperDialog(object):

	def btnOpen_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_OK)

	def btnCancel_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_CANCEL)

	def openDialog(self, Option, Config, Ws, images):
		self.Dialog.show_all()
		result = self.Dialog.run()
		if (result == gtk.RESPONSE_OK):
#TODO:ホントは値あるなし,PATH有効かなど、チェックがいる
			AppletUtil.setCoreArg(Option, Config, Ws)
			Option.args[0] = images[0]
			Option.args[1] = images[1]
			Option.opts.save = self.Dialog.get_filename()
			Core = Core(Applet.logging)
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

class Applet(object):

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
	images = ['','']

	def setConfigAttr(self, btnName):
		if (btnName.find('PushLeft') > 0 or btnName.find('PushRight') > 0):
			attr = 'align'
		elif (btnName.find('Upper') > 0 or btnName.find('Lower') > 0):
			attr = 'valign'
		return attr

	def tglBtn_pressed(self, widget):
		vsName = Applet.mapdic[widget.get_name()]
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
			lr = AppletUtil.judgeLeftRight(wName)
			Applet.config[attr][lr] = val

	def tglBtn_released(self, widget):
		vsName = Applet.mapdic[widget.get_name()]
		if (widget.get_active() == False and self.wTree.get_widget(vsName).get_active() == False):
			wName = widget.get_name()
			attr = self.setConfigAttr(wName)
			if (attr == 'align'):
				val = 'center'
			elif (attr == 'valign'):
				val = 'middle'
			lr = AppletUtil.judgeLeftRight(wName)
			Applet.config[attr][lr] = val

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
		Applet.config['mergin'][idx] = int(self.wTree.get_widget(wName).get_text())

	def radFixed_toggled(self, widget):
		wName = widget.get_name()
		Applet.config['fixed'] = self.wTree.get_widget(wName).get_active()

	def btnGetImg_clicked(self, widget):
		wName = widget.get_name()
		lr = AppletUtil.judgeLeftRight(wName)
		ImgOpenDialog = ImgOpenDialog(self.gladefile, self.logging)
		Applet.images[lr] = ImgOpenDialog.openDialog()
		if (lr == 0):
			self.wTree.get_widget('entPathL').set_text(Applet.images[lr])
		else:
			self.wTree.get_widget('entPathR').set_text(Applet.images[lr])

	def entImgPath_activate(self, widget):
		wName = widget.get_name()
		lr = AppletUtil.judgeLeftRight(wName)
		Applet.images[lr] = os.path.expanduser(self.wTree.get_widget(wName).get_text())
		if (lr == 0):
			self.wTree.get_widget('entPathL').set_text(Applet.images[lr])
		else:
			self.wTree.get_widget('entPathR').set_text(Applet.images[lr])
#TODO: 拡張子チェック?

	def btnSetting_clicked(self, widget):
		SettingDialog = SettingDialog(self.gladefile, self.logging)
		SettingDialog.openDialog(Applet.config['display'], Applet.config['srcdir'])

	def btnSetColor_clicked(self, widget):
		ColorSelectionDialog = ColorSelectionDiag(self.gladefile ,self.logging)
		ColorSelectionDialog.openDialog(Applet.config['bgcolor'])

	def btnSave_clicked(self, widget):
		SaveWallpaperDialog = SaveWallpaperDialog(self.gladefile, self.logging)
		SaveWallpaperDialog.openDialog(self.Option, self.Config, self.Ws, Applet.images)

	def btnSetWall_clicked(self, widget):
		AppletUtil.setCoreArg(self.Option, self.Config, self.Ws)
		self.Option.args[0] = Applet.images[0]
		self.Option.args[1] = Applet.images[1]
		self.Option.opts.setWall = True
		Core = Core(self.logging)
		Core.singlerun(self.Option, self.Config, self.Ws)

	def entInterval_activate(self, widget):
		wName = widget.get_name()
		Applet.option['interval'] = int(self.wTree.get_widget(wName).get_value())

	def _runChanger(self):
		AppletUtil.setCoreArg(self.Option, self.Config, self.Ws)
		Core = Core(self.logging)
		self.seed = Core.timerRun(self.Option, self.Config, self.Ws, self.seed)

	def _timeout(self, widget):
		print "Timeout"
		self._runChanger()
		return True

	def btnDaemonize_clicked(self, widget):
		self._runChanger()
		self.timeoutObject = gobject.timeout_add(Applet.option['interval']*1000, self._timeout, self)

	def btnCancelDaemonize_clicked(self, widget):
		print "Cancel"
		gobject.source_remove(self.timeoutObject)
		self.timeoutObject = None

	def __init__(self, Option, Config, Ws, logger):
		self.Option = Option
		self.Config = Config
		self.Ws = Ws
		self.logging = logger

		self.Option.args = ['','']
		AppletUtil.setAppletConfig(self.Option, self.Config, self.Ws)

		self.timeoutObject = None
		self.seed = 1

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
			"on_btnCancelDamonize_clicked" : self.btnCancelDaemonize_clicked,
			"on_btnQuit_clicked" : gtk.main_quit,
			"on_WallPosit_MainWindow_destroy" : gtk.main_quit
			}
		self.wTree.signal_autoconnect(dic)

	def finalize(self):
		gtk.main()
