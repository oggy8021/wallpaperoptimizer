# -*- coding: utf-8 -*-

class AppletUtil(object):
	@staticmethod
	def judgeLeftRight(wName):
		if wName.rfind('L') == (len(wName) - 1):
			idx = 0
		elif wName.rfind('R') == (len(wName) - 1):
			idx = 1
		return idx

	@staticmethod
	def writeStatusbar(bar, cid, msg):
		bar.push(cid, msg)

	@staticmethod
	def eraseStatusbar(bar, cid):
		bar.pop(cid)

	@staticmethod
	def runErrorDialog(self, msg):
		errorDialog = ErrorDialog(self.gladefile)
		errorDialog.openDialog(msg)
