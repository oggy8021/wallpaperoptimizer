# -*- coding: utf-8 -*-

import csv
import os.path

import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

from WallpaperOptimizer.Widget.DialogBase import DialogBase
from WallpaperOptimizer.Widget.ErrorDialog import ErrorDialog
from WallpaperOptimizer.Widget.SrcdirDialog import SrcdirDialog

class SettingDialog(DialogBase):

	def _runErrorDialog(self, msg):
		errorDialog = ErrorDialog(self.gladefile)
		errorDialog.openDialog(msg)

	def _judgeLeftRight(self, wName):
		if wName.rfind('L') == (len(wName) - 1):
			idx = 0
		elif wName.rfind('R') == (len(wName) - 1):
			idx = 1
		return idx

	def _setSize(self, strlr):
		width = self.walkTree.get_widget('entDisplayW' + strlr).get_text()
		height = self.walkTree.get_widget('entDisplayH' + strlr).get_text()
		if width == '':
			width = '0'
		if height == '':
			height = '0'
		return [int(width), int(height)]

	def _getSettingDialog(self, pos):
		if pos == 'left':
			strlr = 'L'
		elif pos == 'right':
			strlr = 'R'
		return [str(self._setSize(strlr)[0]) + 'x' + str(self._setSize(strlr)[1])
				 , pos
				 , self.walkTree.get_widget('entSrcdir' + strlr).get_text()]

	def btnOpenSrcdir_clicked(self, widget):
		lr = self._judgeLeftRight(widget.get_name())
		srcdirDialog = SrcdirDialog(self.gladefile)
		retdir = srcdirDialog.openDialog(self.srcdirs[lr], lr)
		if not retdir == False:
			if lr == 0:
				strlr = 'L'
			else:
				strlr = 'R'
			self.srcdirs[lr] = retdir
			self.walkTree.get_widget('entSrcdir' + strlr).set_text(self.srcdirs[lr])

	def btnSaveSetting_clicked(self, widget):
		configfile='~/.walloptrc'
		try:
			cf = csv.writer(file(os.path.abspath(os.path.expanduser(configfile)), 'w'))
			cf.writerow(self._getSettingDialog('left'))
			cf.writerow(self._getSettingDialog('right'))
		except IOError, msg:
			self._runErrorDialog('** CoreRuntimeError: %s. ' % msg)

	def btnClear_clicked(self, widget):
		self._setSettingDialogWidget([0,0], [0,0], ['',''])

	def _setSettingDialogWidget(self, lDisplaySize, rDisplaySize, srcdirs):
		for lr in (0,1):
			if lr == 0:
				strlr = 'L'
				displaySize = lDisplaySize
			else:
				strlr = 'R'
				displaySize = rDisplaySize
			for wh in (0,1):
				if wh == 0:
					strwh = 'W'
				else:
					strwh = 'H'
				self.walkTree.get_widget('entDisplay' + strwh + strlr).set_text(str(displaySize[wh]))
			self.walkTree.get_widget('entSrcdir' + strlr).set_text(self.srcdirs[lr])

	def openDialog(self, lDisplaySize, rDisplaySize, srcdirs):
		self.lDisplaySize = lDisplaySize
		self.rDisplaySize = rDisplaySize
		self.srcdirs = srcdirs

		self.Dialog.show_all()
		self._setSettingDialogWidget(self.lDisplaySize, self.rDisplaySize, self.srcdirs)

		result = self.Dialog.run()
		if result == gtk.RESPONSE_OK:
			self.lDisplaySize = self._setSize('L')
			self.rDisplaySize = self._setSize('R')
			self.srcdirs = [
				self.walkTree.get_widget('entSrcdirL').get_text()
				 ,
				self.walkTree.get_widget('entSrcdirR').get_text()
				 ]
			self.Dialog.destroy()
			return [self.lDisplaySize, self.rDisplaySize, self.srcdirs]
		else:
			self.Dialog.destroy()
			return [False, False, False]

	def __init__(self, gladefile):
		self.gladefile = gladefile
		[self.walkTree, self.Dialog] = self.loadGladeTree(self.gladefile, "SettingDialog")

		dic = {
			"on_btnOpenSrcdir_clicked" : self.btnOpenSrcdir_clicked,
			"on_btnClear_clicked" : self.btnClear_clicked,
			"on_btnSaveSetting_clicked" : self.btnSaveSetting_clicked,
			"on_btnOk_clicked" : self.btnOk_clicked,
			"on_btnCancel_clicked" : self.btnCancel_clicked,
			"on_SettingDialog_destroy" : self.btnCancel_clicked
			}
		self.walkTree.signal_autoconnect(dic)
