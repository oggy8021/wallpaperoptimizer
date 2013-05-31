# -*- coding: utf-8 -*-

import os.path
import WallpaperOptimizer

from WallpaperOptimizer.Widget.ErrorDialog import ErrorDialog

#from nose.tools import ok_, eq_

def Error_test():
	gladefile = os.path.abspath(os.path.join(WallpaperOptimizer.LIBRARYDIR,'glade','wallpositapplet.glade'))
	msg = 'hoge'

	errorDialog = ErrorDialog(gladefile)
	errorDialog.openDialog(msg)

if __name__ == "__main__":
	Error_test()