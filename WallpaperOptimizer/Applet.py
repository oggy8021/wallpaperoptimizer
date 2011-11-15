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
try:
	import glib as glibobj
except:
	try:
		import gobject as glibobj
	except:
		sys.exit(2)

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
		return [self.walkTree.get_widget('entDisplayW' + lr).get_text()
				 + 'x'
				 + self.walkTree.get_widget('entDisplayH' + lr).get_text()
				 , 'left'
				 , self.walkTree.get_widget('entSrcdir' + lr).get_text()
				 ]

	@staticmethod
	def setCoreArg(Option, Config, Ws):
		Option.opts.align = Applet.config['align']
		Option.opts.valign = Applet.config['valign']
		Option.opts.mergin = Applet.config['mergin']
		Option.opts.fixed = Applet.config['fixed']
		Option.opts.bgcolor = Applet.config['bgcolor']
		Option.opts.interval = Applet.option['interval']

		lWidthHeight = Applet.config['display'][0].split('x')
		Config.lDisplay.setConfig(int(lWidthHeight[0]),
										int(lWidthHeight[1]),
										Config.lDisplay.getConfig()['posit'],
										Applet.config['srcdir'][0])
		rWidthHeight = Applet.config['display'][1].split('x')
		Config.rDisplay.setConfig(int(rWidthHeight[0]),
										int(rWidthHeight[1]),
										Config.rDisplay.getConfig()['posit'],
										Applet.config['srcdir'][1])
		Ws.setScreenSize(
							[int(lWidthHeight[0]), int(lWidthHeight[1])], 
							[int(rWidthHeight[0]), int(rWidthHeight[1])]
							)
		Ws.compareToScreen()
		Ws.setScreenType()

	@staticmethod
	def writeStatusbar(bar, cid, msg):
		bar.push(cid, msg)

	@staticmethod
	def eraseStatusbar(bar, cid):
		bar.pop(cid)

	@staticmethod
	def initWidget(self):
		self.tglPushLeftL = self.walkTree.get_widget('tglPushLeftL')
		self.tglPushRightL = self.walkTree.get_widget('tglPushRightL')
		self.tglUpperL = self.walkTree.get_widget('tglUpperL')
		self.tglLowerL = self.walkTree.get_widget('tglLowerL')
		self.btnGetImgL = self.walkTree.get_widget('btnGetImgL')
		self.entPathL = self.walkTree.get_widget('entPathL')

		self.tglPushLeftR = self.walkTree.get_widget('tglPushLeftR')
		self.tglPushRightR = self.walkTree.get_widget('tglPushRightR')
		self.tglUpperR = self.walkTree.get_widget('tglUpperR')
		self.tglLowerR = self.walkTree.get_widget('tglLowerR')
		self.btnGetImgR = self.walkTree.get_widget('btnGetImgR')
		self.entPathR = self.walkTree.get_widget('entPathR')

		self.spnLMergin = self.walkTree.get_widget('spnLMergin')
		self.spnRMergin = self.walkTree.get_widget('spnRMergin')
		self.spnTopMergin = self.walkTree.get_widget('spnTopMergin')
		self.spnBtmMergin = self.walkTree.get_widget('spnBtmMergin')
		self.radXinerama = self.walkTree.get_widget('radXinerama')
		self.radTwinView = self.walkTree.get_widget('radTwinView')
		self.radFixed = self.walkTree.get_widget('radFixed')
		self.radNoFixed = self.walkTree.get_widget('radNoFixed')

		self.btnSetting = self.walkTree.get_widget('btnSetting')
		self.btnSetColor = self.walkTree.get_widget('btnSetColor')
		self.btnSave = self.walkTree.get_widget('btnSave')
		self.btnSetWall = self.walkTree.get_widget('btnSetWall')
		self.spnInterval = self.walkTree.get_widget('spnInterval')
		self.btnDaemonize = self.walkTree.get_widget('btnDaemonize')
		self.btnCancelDaemonize = self.walkTree.get_widget('btnCancelDaemonize')
		self.btnQuit = self.walkTree.get_widget('btnQuit')
		self.btnHelp = self.walkTree.get_widget('btnHelp')
		self.btnAbout = self.walkTree.get_widget('btnAbout')
		self.statbar = self.walkTree.get_widget('statusbar')

	@staticmethod
	def switchWidget(self, boolean):
		self.tglPushLeftL.set_sensitive(boolean)
		self.tglPushRightL.set_sensitive(boolean)
		self.tglUpperL.set_sensitive(boolean)
		self.tglLowerL.set_sensitive(boolean)
		self.btnGetImgL.set_sensitive(boolean)
		self.entPathL.set_sensitive(boolean)
		self.tglPushLeftR.set_sensitive(boolean)
		self.tglPushRightR.set_sensitive(boolean)
		self.tglUpperR.set_sensitive(boolean)
		self.tglLowerR.set_sensitive(boolean)
		self.btnGetImgR.set_sensitive(boolean)
		self.entPathR.set_sensitive(boolean)
		self.spnLMergin.set_sensitive(boolean)
		self.spnRMergin.set_sensitive(boolean)
		self.spnTopMergin.set_sensitive(boolean)
		self.spnBtmMergin.set_sensitive(boolean)
#		self.radXinerama.set_sensitive(boolean)
#		self.radTwinView.set_sensitive(boolean)
		self.radFixed.set_sensitive(boolean)
		self.radNoFixed.set_sensitive(boolean)
		self.btnSetting.set_sensitive(boolean)
		self.btnSetColor.set_sensitive(boolean)
		self.btnSave.set_sensitive(boolean)
		self.btnSetWall.set_sensitive(boolean)
		self.spnInterval.set_sensitive(boolean)
		self.btnDaemonize.set_sensitive(boolean)
#		self.btnCancelDaemonize.set_sensitive(boolean)
#		self.btnQuit.set_sensitive(boolean)
#		self.btnHelp.set_sensitive(boolean)
		self.btnAbout.set_sensitive(boolean)


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

	def __init__(self, gladefile):
		self.walkTree = gtk.glade.XML(gladefile, "ImgOpenDialog")
		self.Dialog = self.walkTree.get_widget("ImgOpenDialog")
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
		self.walkTree.signal_autoconnect(dic)


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

	def __init__(self, gladefile):
		self.walkTree = gtk.glade.XML(gladefile, "SrcDirDialog")
		self.Dialog = self.walkTree.get_widget("SrcDirDialog")

		dic = {
			"on_btnOpen_clicked" : self.btnOpen_clicked,
			"on_btnCancel_clicked" : self.btnCancel_clicked,
			"on_SrcdirDialog_destroy" : self.btnCancel_clicked
			}
		self.walkTree.signal_autoconnect(dic)


class SettingDialog(object):

	def btnOpenSrcdir_clicked(self, widget):
		wName = widget.get_name()
		lr = AppletUtil.judgeLeftRight(wName)
		srcdirDialog = SrcdirDialog(self.gladefile)
		self.srcdirs[lr] = srcdirDialog.openDialog(self.srcdirs[lr])
		if (lr == 0):
			self.walkTree.get_widget('entSrcdirL').set_text(self.srcdirs[lr])
		else:
			self.walkTree.get_widget('entSrcdirR').set_text(self.srcdirs[lr])

	def btnSaveSetting_clicked(self, widget):
#dummy
		configfile='~/Develop/WallPosit/trunk/.wallpositrc_gui'
		cf = csv.writer(file(os.path.expanduser(configfile), 'w'))
		cf.writerow(AppletUtil.getSettingDialog(0))
		cf.writerow(AppletUtil.getSettingDialog(1))

	def btnClear_clicked(self, widget):
		self.walkTree.get_widget('entDisplayWL').set_text('')
		self.walkTree.get_widget('entDisplayHL').set_text('')
		self.walkTree.get_widget('entDisplayWR').set_text('')
		self.walkTree.get_widget('entDisplayHR').set_text('')
		self.walkTree.get_widget('entSrcdirL').set_text('')
		self.walkTree.get_widget('entSrcdirR').set_text('')

	def btnOk_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_OK)

	def btnCancel_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_CANCEL)

	def openDialog(self, displays, srcdirs):
		self.srcdirs = srcdirs

		self.Dialog.show_all()
		disp = displays[0].split('x')
		self.walkTree.get_widget('entDisplayWL').set_text(disp[0])
		self.walkTree.get_widget('entDisplayHL').set_text(disp[1])
		disp = displays[1].split('x')
		self.walkTree.get_widget('entDisplayWR').set_text(disp[0])
		self.walkTree.get_widget('entDisplayHR').set_text(disp[1])
		self.walkTree.get_widget('entSrcdirL').set_text(srcdirs[0])
		self.walkTree.get_widget('entSrcdirR').set_text(srcdirs[1])
		result = self.Dialog.run()
		if (result == gtk.RESPONSE_OK):
			Applet.config['display'] = [
				self.walkTree.get_widget('entDisplayWL').get_text()
				 + 'x' 
				 + self.walkTree.get_widget('entDisplayHL').get_text()
				 ,
				self.walkTree.get_widget('entDisplayWR').get_text()
				 + 'x' 
				 + self.walkTree.get_widget('entDisplayHR').get_text()
				 ]
			Applet.config['srcdir'] = [
				self.walkTree.get_widget('entSrcdirL').get_text()
				 ,
				self.walkTree.get_widget('entSrcdirR').get_text()
				 ]
		self.Dialog.destroy()

	def __init__(self, gladefile):
		self.gladefile = gladefile
		self.walkTree = gtk.glade.XML(gladefile, "SettingDialog")
		self.Dialog = self.walkTree.get_widget("SettingDialog")

		dic = {
			"on_btnOpenSrcdir_clicked" : self.btnOpenSrcdir_clicked,
			"on_btnClear_clicked" : self.btnClear_clicked,
			"on_btnSaveSetting_clicked" : self.btnSaveSetting_clicked,
			"on_btnOk_clicked" : self.btnOk_clicked,
			"on_btnCancel_clicked" : self.btnCancel_clicked,
			"on_SettingDialog_destroy" : self.btnCancel_clicked
			}
		self.walkTree.signal_autoconnect(dic)


class ColorSelectionDiag(object):

	def btnOk_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_OK)

	def btnCancel_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_CANCEL)

	def openDialog(self, bgcolor):
		self.Dialog.show_all()
		gdkColor = gtk.gdk.Color()
		gdkColor = gtk.color_selection_palette_from_string(bgcolor)
		self.walkTree.get_widget('color_selection').set_current_color(gdkColor[0])
		result = self.Dialog.run()
		if (result == gtk.RESPONSE_OK):
			gtkColor = self.walkTree.get_widget('color_selection').get_current_color()
			bgcolor = gtk.color_selection_palette_to_string([gtkColor])
		self.Dialog.destroy()
		Applet.config['bgcolor'] = bgcolor

	def __init__(self, gladefile):
		self.walkTree = gtk.glade.XML(gladefile, "ColorSelectionDialog")
		self.Dialog = self.walkTree.get_widget("ColorSelectionDialog")

		dic = {
			"on_btnOk_clicked" : self.btnOk_clicked,
			"on_btnCancel_clicked" : self.btnCancel_clicked,
			"on_ColorSelectionDialog_destroy" : self.btnCancel_clicked,
			}
		self.walkTree.signal_autoconnect(dic)


class SaveWallpaperDialog(object):

	def btnOpen_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_OK)

	def btnCancel_clicked(self, widget):
		self.Dialog.response(gtk.RESPONSE_CANCEL)

	def openDialog(self, Option, Config, Ws, images, logger):
		self.Dialog.show_all()
		result = self.Dialog.run()
		if (result == gtk.RESPONSE_OK):
#TODO:ホントは値あるなし,PATH有効かなど、チェックがいる
			AppletUtil.setCoreArg(Option, Config, Ws)
			Option.args[0] = images[0]
			Option.args[1] = images[1]
			Option.opts.save = self.Dialog.get_filename()
			core = Core(logger)
			core.singlerun(Option, Config, Ws)
		self.Dialog.destroy()

	def __init__(self, gladefile):
		self.gladefile = gladefile
		self.walkTree = gtk.glade.XML(gladefile, "SaveWallpaperDialog")
		self.Dialog = self.walkTree.get_widget("SaveWallpaperDialog")

		dic = {
			"on_btnOpen_clicked" : self.btnOpen_clicked,
			"on_btnCancel_clicked" : self.btnCancel_clicked,
			"on_SaveWallpaperDialog_destroy" : self.btnCancel_clicked
			}
		self.walkTree.signal_autoconnect(dic)

class Applet(object):

	tgldic = dict()
	tgldic['tglPushLeftL'] = 'tglPushRightL'
	tgldic['tglPushRightL'] = 'tglPushLeftL'
	tgldic['tglUpperL'] = 'tglLowerL'
	tgldic['tglLowerL'] = 'tglUpperL'
	tgldic['tglPushLeftR'] = 'tglPushRightR'
	tgldic['tglPushRightR'] = 'tglPushLeftR'
	tgldic['tglUpperR'] = 'tglLowerR'
	tgldic['tglLowerR'] = 'tglUpperR'

	config = dict()
	config['align'] = ['center','center']
	config['valign'] = ['middle','middle']
	config['mergin'] = [0,0,0,0]
	config['fixed'] = True
	#TODO:str,int行ったり来たり
	config['display'] = ['1024x768','1024x768']
	config['bgcolor'] = 'black'
	config['srcdir'] = ['','']
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
		vsName = Applet.tgldic[widget.get_name()]
		if (self.walkTree.get_widget(vsName).get_active()):
			self.walkTree.get_widget(vsName).set_active(False)

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
		vsName = Applet.tgldic[widget.get_name()]
		if (widget.get_active() == False and 
				self.walkTree.get_widget(vsName).get_active() == False):
			wName = widget.get_name()
			attr = self.setConfigAttr(wName)
			if (attr == 'align'):
				val = 'center'
			elif (attr == 'valign'):
				val = 'middle'
			lr = AppletUtil.judgeLeftRight(wName)
			Applet.config[attr][lr] = val

	def spnMergin_value_changed(self, widget):
		wName = widget.get_name()
		if (wName.find('LMergin')) > 0:
			idx = 0
		elif (wName.find('RMergin')) > 0:
			idx = 1
		elif (wName.find('TopMergin')) > 0:
			idx = 2
		elif (wName.find('BtmMergin')) > 0:
			idx = 3
		Applet.config['mergin'][idx] = int(self.walkTree.get_widget(wName).get_value_as_int())

	def radFixed_toggled(self, widget):
		wName = widget.get_name()
		Applet.config['fixed'] = self.walkTree.get_widget(wName).get_active()

	def btnGetImg_clicked(self, widget):
		wName = widget.get_name()
		lr = AppletUtil.judgeLeftRight(wName)
		imgopenDialog = ImgOpenDialog(self.gladefile)
		Applet.images[lr] = imgopenDialog.openDialog()
		if (lr == 0):
			self.entPathL.set_text(Applet.images[lr])
		else:
			self.entPathR.set_text(Applet.images[lr])

	def btnSetting_clicked(self, widget):
		settingDialog = SettingDialog(self.gladefile)
		settingDialog.openDialog(Applet.config['display'], Applet.config['srcdir'])

	def btnSetColor_clicked(self, widget):
		colorselectionDialog = ColorSelectionDiag(self.gladefile)
		colorselectionDialog.openDialog(Applet.config['bgcolor'])

	def btnSave_clicked(self, widget):
		savewallpaperDialog = SaveWallpaperDialog(self.gladefile)
		savewallpaperDialog.openDialog(self.Option, self.Config, self.Ws, Applet.images, self.logging)

	def btnSetWall_clicked(self, widget):
		AppletUtil.setCoreArg(self.Option, self.Config, self.Ws)
		self.Option.args[0] = Applet.images[0]
		self.Option.args[1] = Applet.images[1]
		self.Option.opts.setWall = True
		core = Core(self.logging)
		core.singlerun(self.Option, self.Config, self.Ws)

	def spnInterval_value_changed(self, widget):
		Applet.option['interval'] = self.spnInterval.get_value_as_int()
		AppletUtil.eraseStatusbar(self.statbar, self.cid_stat)
		AppletUtil.writeStatusbar(self.statbar
				, self.cid_stat
				, 'Change Interval ... %d sec.' % Applet.option['interval'])

	def _runChanger(self):
		core = Core(self.logging)
		self.seed = core.timerRun(self.Option, self.Config, self.Ws, self.seed)

	def _timeout(self, applet):
		self.logging.debug('%20s at %d sec.' % ('Timeout', Applet.option['interval']))
		AppletUtil.eraseStatusbar(self.statbar, self.cid_stat)
		AppletUtil.writeStatusbar(self.statbar
				, self.cid_stat
				, 'Timeout ... run changer.')
		self._runChanger()
		if (self.canceled):
			return False
		else:
			return True

	def btnDaemonize_clicked(self, widget):
		self.canceled = False
		AppletUtil.switchWidget(self, False)
		self.btnCancelDaemonize.set_sensitive(True)
		AppletUtil.setCoreArg(self.Option, self.Config, self.Ws)
		self.timeoutObject = glibobj.timeout_add(Applet.option['interval']*1000
				, self._timeout, self)
		self.logging.debug('%20s' % 'Start Daemonize ... interval [%d].' % Applet.option['interval'])
		self._runChanger()

	def btnCancelDaemonize_clicked(self, widget):
		self.canceled = True
		glibobj.source_remove(self.timeoutObject)
		self.timeoutObject = None
		AppletUtil.writeStatusbar(self.statbar, self.cid_stat, 'Cancel ... changer action.')
		AppletUtil.switchWidget(self, True)
		self.btnCancelDaemonize.set_sensitive(False)

	def __init__(self, Option, Config, Ws, logger):
		self.logging = logger
		self.Option = Option
		self.Config = Config
		self.Ws = Ws
		self.Option.args = ['','']

		self.gladefile = os.path.abspath("./WallpaperOptimizer/glade/wallpositapplet.glade")
		self.walkTree = gtk.glade.XML(self.gladefile, "WallPosit_MainWindow")
		self.window = self.walkTree.get_widget("WallPosit_MainWindow")
		AppletUtil.initWidget(self)
		self.btnCancelDaemonize.set_sensitive(False)

		AppletUtil.setAppletConfig(self.Option, self.Config, self.Ws)
		self.timeoutObject = None
		self.seed = 1
		self.canceled = False
		self.cid_stat = self.statbar.get_context_id('status')
		self.cid_err = self.statbar.get_context_id('error')

# 未実装ボタン
		self.radXinerama.set_sensitive(False)
		self.radTwinView.set_sensitive(False)
		self.btnHelp.set_sensitive(False)
		self.btnAbout.set_sensitive(False)

		AppletUtil.writeStatusbar(self.statbar, self.cid_stat, 'Running ... applet mode.')

		dic = {
			"on_tglBtn_pressed" : self.tglBtn_pressed,
			"on_tglBtn_toggled" : self.tglBtn_toggled,
			"on_tglBtn_released" : self.tglBtn_released,
			"on_spnMergin_value_changed" : self.spnMergin_value_changed,
			"on_radFixed_toggled" : self.radFixed_toggled,
			"on_btnGetImg_clicked" : self.btnGetImg_clicked,
			"on_btnSetting_clicked" : self.btnSetting_clicked,
			"on_btnSetColor_clicked" : self.btnSetColor_clicked,
			"on_btnSave_clicked" : self.btnSave_clicked,
			"on_btnSetWall_clicked" : self.btnSetWall_clicked,
			"on_spnInterval_value_changed" : self.spnInterval_value_changed,
			"on_btnDaemonize_clicked" : self.btnDaemonize_clicked,
			"on_btnCancelDaemonize_clicked" : self.btnCancelDaemonize_clicked,
			"on_btnQuit_clicked" : gtk.main_quit,
			"on_WallPosit_MainWindow_destroy" : gtk.main_quit
			}
		self.walkTree.signal_autoconnect(dic)

	def finalize(self):
		gtk.main()
