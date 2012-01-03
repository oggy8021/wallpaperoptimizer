# -*- coding: utf-8 -*-

import sys
import os.path
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
import gnomeapplet
import gnome.ui
from distutils.sysconfig import PREFIX, get_python_lib

from WallpaperOptimizer.Core import Core
from WallpaperOptimizer.OptionsBase import OptionsBase
from WallpaperOptimizer.Widget.ErrorDialog import ErrorDialog
from WallpaperOptimizer.Widget.ImgOpenDialog import ImgOpenDialog
from WallpaperOptimizer.Widget.SettingDialog import SettingDialog
from WallpaperOptimizer.Widget.ColorSelectionDialog import ColorSelectionDialog
from WallpaperOptimizer.Widget.SaveWallpaperDialog import SaveWallpaperDialog

class AppletOptions(OptionsBase):

	class Opts(object):
		def __init__(self):
			self.align = ['center','center']
			self.valign = ['middle','middle']
			self.mergin = [0,0,0,0]
			self.fixed = True
			self.size = [None,None]
			self.bgcolor = 'black'
			self.srcdir = ['','']
			self.verbose = False
			self.save=None
			self.setWall=False
			self.daemonize=False
			self.interval = 60
			self.combine = True

	def getWindow(self):
		return True

	def __init__(self):
		self.opts = AppletOptions.Opts()
		self.args = ['','']


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

	def _runErrorDialog(self, msg):
		errorDialog = ErrorDialog(self.gladefile)
		errorDialog.openDialog(msg)

#utility group
	def _judgeLeftRight(self, wName):
		if wName.rfind('L') == (len(wName) - 1):
			idx = 0
		elif wName.rfind('R') == (len(wName) - 1):
			idx = 1
		return idx

	def _writeStatusbar(self, bar, cid, msg):
		bar.push(cid, msg)

	def _eraseStatusbar(self, bar, cid):
		bar.pop(cid)

	def _setConfigAttr(self, btnName, lr, val=None):
		if (btnName.find('PushLeft') > 0 or btnName.find('PushRight') > 0):
			if val == None:
				val = 'center'
			self.option.opts.align[lr] = val
		elif (btnName.find('Upper') > 0 or btnName.find('Lower') > 0):
			if val == None:
				val = 'middle'
			self.option.opts.valign[lr] = val

#button group
	def tglBtn_pressed(self, widget):
		vsName = Applet.tgldic[widget.get_name()]
		if (self.walkTree.get_widget(vsName).get_active()):
			self.walkTree.get_widget(vsName).set_active(False)

	def tglBtn_toggled(self, widget):
		if widget.get_active():
			wName = widget.get_name()
			if wName.find('PushLeft') > 0:
				val = 'left'
			elif wName.find('PushRight') > 0:
				val = 'right'
			elif wName.find('Upper') > 0:
				val = 'top'
			elif wName.find('Lower') > 0:
				val = 'bottom'
			lr = self._judgeLeftRight(wName)
			self._setConfigAttr(wName, lr, val)

	def tglBtn_released(self, widget):
		vsName = Applet.tgldic[widget.get_name()]
		if (widget.get_active() == False and 
				self.walkTree.get_widget(vsName).get_active() == False):
			wName = widget.get_name()
			lr = self._judgeLeftRight(wName)
			self._setConfigAttr(wName, lr)

	def spnMergin_value_changed(self, widget):
		wName = widget.get_name()
		if wName.find('LMergin') > 0:
			idx = 0
		elif wName.find('RMergin') > 0:
			idx = 1
		elif wName.find('TopMergin') > 0:
			idx = 2
		elif wName.find('BtmMergin') > 0:
			idx = 3
		self.option.opts.mergin[idx] = int(self.walkTree.get_widget(wName).get_value_as_int())

	def radFixed_toggled(self, widget):
		if widget.get_name() == 'radFixed':
			self.option.opts.fixed = self.walkTree.get_widget(widget.get_name()).get_active()

	def radCombine_toggled(self, widget):
		if widget.get_name() == 'radCombine':
			self.option.opts.combine = self.walkTree.get_widget(widget.get_name()).get_active()

	def btnGetImg_clicked(self, widget):
		lr = self._judgeLeftRight(widget.get_name())
		if lr == 0:
			entPath = self.entPathL
		else:
			entPath = self.entPathR
		if widget.get_name().find('Clr') > 0:
			path = ''
		else:
			imgopenDialog = ImgOpenDialog(self.gladefile)
			path = imgopenDialog.openDialog(self.core.option.args[lr], lr)
		if path <> False:
			self.core.option.args[lr] = path
			entPath.set_text(os.path.basename(path))

	def entPath_insert(self, widget, text, length, pos):
		lr = self._judgeLeftRight(widget.get_name())
		if length > 0:
			self.bEntryPath[lr] = True
		else:
			self.bEntryPath[lr] = False
		if self.bEntryPath == [True, True]:
			self.btnSave.set_sensitive(True)
		elif self.bEntryPath == [True, False] or self.bEntryPath == [False, True]:
			self.btnSetWall.set_sensitive(True)
		else:
			self.btnSetWall.set_sensitive(False)

	def btnSetting_clicked(self, widget):
		settingDialog = SettingDialog(self.gladefile)
		settingArgs = settingDialog.openDialog([
					self.core.config.lDisplay.getConfig()['width']
					, self.core.config.lDisplay.getConfig()['height']
					],[
					self.core.config.rDisplay.getConfig()['width']
					, self.core.config.rDisplay.getConfig()['height']
					],[
					self.core.config.lDisplay.getConfig()['srcdir']
					, self.core.config.rDisplay.getConfig()['srcdir']
					])
		if not settingArgs == [False, False, False]:
			for lr in (0,1):
				if lr == 0:
					display = self.core.config.lDisplay
					displaysize = settingArgs[0] #lDisplaySize
				else:
					display = self.core.config.rDisplay
					displaysize = settingArgs[1] #rDisplaySize
				for wh in (0,1):
					display.setWidth(displaysize[wh])
					display.setHeight(displaysize[wh])
				display.setSrcdir(settingArgs[2][lr])
			self.core.config.checkBool()
			if self.core.config.getBool():
				self.btnDaemonize.set_sensitive(True)
			else:
				self.btnDaemonize.set_sensitive(False)
		else:
			pass

	def btnSetColor_clicked(self, widget):
		colorselectionDialog = ColorSelectionDialog(self.gladefile)
		self.option.opts.bgcolor = colorselectionDialog.openDialog(self.option.opts.bgcolor)

	def btnSave_clicked(self, widget):
		savewallpaperDialog = SaveWallpaperDialog(self.gladefile)
		self.core.option.opts.save = savewallpaperDialog.openDialog()
		if self.core.option.getSavePath() <> None:
#TODO:ホントは値あるなし,PATH有効かなど、チェックがいる
			self._presetCore()
			try:
				self.core.singlerun()
			except self.core.CoreRuntimeError, msg:
				logger.error('** CoreRuntimeError: %s. ' % msg.value)
				self._runErrorDialog(self, '** CoreRuntimeError: %s. ' % msg.value)
		else:
#TODO:エラーメッセージがあると良い
			pass

	def btnSetWall_clicked(self, widget):
		self._presetCore()
		self.core.option.opts.setWall = True
		try:
			self.core.singlerun()
		except self.core.CoreRuntimeError, msg:
			self.logging.error('** CoreRuntimeError: %s. ' % msg.value)
			self._runErrorDialog(self, '** CoreRuntimeError: %s. ' % msg.value)

	def spnInterval_value_changed(self, widget):
		self.option.opts.interval = self.spnInterval.get_value_as_int()
		self._eraseStatusbar(self.statbar, self.cid_stat)
		self._writeStatusbar(self.statbar
				, self.cid_stat
				, 'Change Interval ... %d sec.' % self.option.opts.interval)

	def _runChanger(self):
		try:
			self.core.timerRun()
		except self.core.CoreRuntimeError, msg:
			self.logging.error('** CoreRuntimeError: %s. ' % msg.value)
			self._runErrorDialog(self, '** CoreRuntimeError: %s. ' % msg.value)

	def _timeout(self, applet):
		self.logging.debug('%20s at %d sec.' % ('Timeout', self.option.opts.interval))
		self._eraseStatusbar(self.statbar, self.cid_stat)
		self._writeStatusbar(self.statbar
				, self.cid_stat
				, 'Timeout ... run changer.')
		self._runChanger()
		if self.bCanceled:
			return False
		else:
			return True

	def btnDaemonize_clicked(self, widget):
		self.bCanceled = False
		self._setPanelButton(self.applet, self.bCanceled)
		self.window.set_icon(self._select_icon(self.bCanceled))
		self._switchWidget(False)
		self.window.hide()
		self.bVisible = False
		self.btnOnTooltip.set_tip(self.applet, 'changer on')
		self._presetCore()
		self.timeoutObject = glibobj.timeout_add(self.option.opts.interval*1000
				, self._timeout, self)
		self.logging.debug('%20s' % 
				'Start Daemonize ... interval [%d].' % self.option.opts.interval)
		self._runChanger()

	def btnCancelDaemonize_clicked(self, widget):
		self.bCanceled = True
		self._setPanelButton(self.applet, self.bCanceled)
		self.window.set_icon(self._select_icon(self.bCanceled))
		self.btnOnTooltip.set_tip(self.applet, 'changer off')
		glibobj.source_remove(self.timeoutObject)
		self.timeoutObject = None
		self._writeStatusbar(self.statbar, self.cid_stat, 'Cancel ... changer action.')
		self._switchWidget(True)

	def btnAbout_clicked(self, widget):
		iconFile = '/WallpaperOptimizer/wallopt.png'
		icon = gtk.gdk.pixbuf_new_from_file(os.path.abspath(os.path.join(PREFIX,'share',iconFile)))
		about = gnome.ui.About("WallpaperOptimizer"
							,"0.1.0.0"	#version
							,"GPLv3"		#copyright
							,"wallpaperoptimizer is multi wallpaper changer."	#comments
							,["oggy"]		#**authors
							,["oggy"]		#**documenters
							,"oggy"		#*translator_credits
							,icon)			#gtk.gdk.Pixbuf
		about.show_all()

	def btnWindowClose_clicked(self, widget, event):
		self.bVisible = False
		self.pos = self.window.get_position()
		return widget.hide_on_delete()

#initialize group
	def _linkGladeTree(self):
		self.tglPushLeftL = self.walkTree.get_widget('tglPushLeftL')
		self.tglPushRightL = self.walkTree.get_widget('tglPushRightL')
		self.tglUpperL = self.walkTree.get_widget('tglUpperL')
		self.tglLowerL = self.walkTree.get_widget('tglLowerL')
		self.btnGetImgL = self.walkTree.get_widget('btnGetImgL')
		self.entPathL = self.walkTree.get_widget('entPathL')
#
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
		self.radCombine = self.walkTree.get_widget('radCombine')
		self.radSeparate = self.walkTree.get_widget('radSeparate')
		self.radFixed = self.walkTree.get_widget('radFixed')
		self.radNoFixed = self.walkTree.get_widget('radNoFixed')
#
		self.btnSetting = self.walkTree.get_widget('btnSetting')
		self.btnSetColor = self.walkTree.get_widget('btnSetColor')
		self.btnSave = self.walkTree.get_widget('btnSave')
		self.btnSetWall = self.walkTree.get_widget('btnSetWall')
		self.spnInterval = self.walkTree.get_widget('spnInterval')
		self.btnDaemonize = self.walkTree.get_widget('btnDaemonize')
		self.btnCancelDaemonize = self.walkTree.get_widget('btnCancelDaemonize')
		self.btnHelp = self.walkTree.get_widget('btnHelp')
		self.btnAbout = self.walkTree.get_widget('btnAbout')
		self.statbar = self.walkTree.get_widget('statusbar')

	def _presetCore(self):
		self.core.Ws.compareToScreen()
		self.core.Ws.setAttrScreenType()

	def _switchWidget(self, boolean):
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
		self.radFixed.set_sensitive(boolean)
		self.radNoFixed.set_sensitive(boolean)
		self.btnSetting.set_sensitive(boolean)
		self.btnSetColor.set_sensitive(boolean)
		self.btnSave.set_sensitive(boolean)
		self.btnSetWall.set_sensitive(boolean)
		self.spnInterval.set_sensitive(boolean)
		self.btnDaemonize.set_sensitive(boolean)
		if boolean:
			self.btnCancelDaemonize.set_sensitive(False)
		else:
			self.btnCancelDaemonize.set_sensitive(True)
		self.radXinerama.set_sensitive(False)
		self.radTwinView.set_sensitive(False)
#	  未実装ボタン
		self.btnHelp.set_sensitive(False)

#panel control group
	def _select_icon(self,bCanceled):
		if bCanceled:
			icon = self.dis_icon
		else:
			icon = self.ena_icon
		return icon

	def _visibleCtrl(self, *arguments):
		if self.bVisible:
			self.window.hide()
			self.bVisible = False
		else:
			self.window.move(self.pos[0], self.pos[1])
			self.window.show_all()
			self.bVisible = True

	def _preferences(self, *arguments):
		self.btnSetting_clicked(None)

	def _selectColor(self, *arguments):
		self.btnSetColor_clicked(None)

	def _about(self, *arguments):
		self.btnAbout_clicked(None)

	def _create_menu(self, applet):
		menuxml="""
			<popup name="button3">
				<menuitem name="Item 2" verb="Visible" label="表示／非表示" pixtype="stock" pixname="gtk-execute"/>
				<menuitem name="Item 3" verb="Preferences" label="設定" pixtype="stock" pixname="gtk-preferences"/>
				<menuitem name="Item 4" verb="Color" label="色選択" pixtype="stock" pixname="gtk-select-color"/>
				<menuitem name="Item 5" verb="About" label="情報" pixtype="stock" pixname="gtk-about"/>
			</popup>"""
#
		verbs = [  ("Visible", self._visibleCtrl )
					, ("Preferences", self._preferences )
					, ("Color", self._selectColor)
					, ("About", self._about)
				]
		applet.setup_menu(menuxml, verbs, None)

	def _setMenu(self, widget, event, applet):
		if event.button == 1:
			if self.core.config.getBool():
				if self.bCanceled:
					self.btnDaemonize_clicked(None)
				else:
					self.btnCancelDaemonize_clicked(None)
			else:
				self._writeStatusbar(self.statbar, self.cid_stat, 'Please set up Config.')
		elif event.button == 3:
			widget.emit_stop_by_name("button-press-event")
			self._create_menu(applet)

	def _setPanelButton(self, applet, bCanceled):
		icon = self._select_icon(bCanceled)
		icon2 = icon.scale_simple(
					icon.get_width() - 4
					, icon.get_width() - 4
					, gtk.gdk.INTERP_BILINEAR )
#!		del icon
		iconOnPanel = gtk.Image()
		iconOnPanel.set_from_pixbuf(icon2)
		self.btnOnPanelBar.set_image(iconOnPanel)

	def _loadIcon(self):
		self.dis_icon = gtk.gdk.pixbuf_new_from_file(os.path.abspath(
				os.path.join(PREFIX,'share','WallpaperOptimizer','wallopt_off.png')))
		self.ena_icon = gtk.gdk.pixbuf_new_from_file(os.path.abspath(
				os.path.join(PREFIX,'share','WallpaperOptimizer','wallopt.png')))


	def __init__(self, applet, iid, logging):
		self.applet = applet
		self.logging = logging
#	  initializeStatus
		self.timeoutObject = None
		self.bVisible = True
		self.bCanceled = True
		self.bEntryPath = [False,False]
#	  Panel initialize
		self.btnOnPanelBar = gtk.Button()
		self.btnOnPanelBar.set_relief(gtk.RELIEF_NONE)
		self._loadIcon()
		self._setPanelButton(self.applet, self.bCanceled)
		self.btnOnPanelBar.connect("button-press-event", self._setMenu, self.applet)
		self.applet.add(self.btnOnPanelBar)
		self.btnOnTooltip = gtk.Tooltips()
		self.btnOnTooltip.set_tip(self.applet, 'changer off')
		self.applet.show_all()
		self.applet.connect("destroy", gtk.main_quit)
#	  AppletOption extends Options class
		self.option = AppletOptions()
		self.core = Core(self.option)
#	  Initialize Applet
		self.gladefile = os.path.abspath(
			os.path.join(get_python_lib(),'WallpaperOptimizer','glade','wallpositapplet.glade'))
#!		self.gladefile = os.path.abspath(
#!			os.path.join('.','WallpaperOptimizer','glade','wallpositapplet.glade'))
		self.walkTree = gtk.glade.XML(self.gladefile, "WallPosit_MainWindow")
		self.window = self.walkTree.get_widget("WallPosit_MainWindow")
		self.window.set_icon(self._select_icon(self.bCanceled))
		self._linkGladeTree()
		self.btnSave.set_sensitive(False)
		self.btnSetWall.set_sensitive(False)
		if not self.core.config.getBool():
			self.btnDaemonize.set_sensitive(False)
		self.btnCancelDaemonize.set_sensitive(False)
		self.cid_stat = self.statbar.get_context_id('status')
#	  bindCallbackFunction
		dic = {
			"on_tglBtn_pressed" : self.tglBtn_pressed,
			"on_tglBtn_toggled" : self.tglBtn_toggled,
			"on_tglBtn_released" : self.tglBtn_released,
			"on_spnMergin_value_changed" : self.spnMergin_value_changed,
			"on_radFixed_toggled" : self.radFixed_toggled,
			"on_radCombine_toggled" : self.radCombine_toggled,
			"on_btnGetImg_clicked" : self.btnGetImg_clicked,
			"on_entPath_insert_text" : self.entPath_insert,
			"on_btnClrPath_clicked" : self.btnGetImg_clicked,
			"on_btnSetting_clicked" : self.btnSetting_clicked,
			"on_btnSetColor_clicked" : self.btnSetColor_clicked,
			"on_btnSave_clicked" : self.btnSave_clicked,
			"on_btnSetWall_clicked" : self.btnSetWall_clicked,
			"on_spnInterval_value_changed" : self.spnInterval_value_changed,
			"on_btnDaemonize_clicked" : self.btnDaemonize_clicked,
			"on_btnCancelDaemonize_clicked" : self.btnCancelDaemonize_clicked,
			"on_btnAbout_clicked" : self.btnAbout_clicked,
			"on_WallPosit_MainWindow_delete_event" : self.btnWindowClose_clicked
			}
		self.walkTree.signal_autoconnect(dic)
#	  未実装ボタン
		self.btnHelp.set_sensitive(False)
#	  View
		self._writeStatusbar(self.statbar, self.cid_stat, 'Running ... applet mode.')
#	  記憶
		self.pos = self.window.get_position()
