# -*- coding: utf-8 -*-

import os.path
import WallpaperOptimizer

from WallpaperOptimizer.Widget.ColorSelectionDialog import ColorSelectionDialog

from nose.tools import ok_, eq_

#画面なので、自動テストはできない？ → 以下のコードでGUI操作可能であった

def SelectRed_test():
	gladefile = os.path.abspath(os.path.join(WallpaperOptimizer.LIBRARYDIR,'glade','wallpositapplet.glade'))
	color = 'black'

	colorselectionDialog = ColorSelectionDialog(gladefile)
	color = colorselectionDialog.openDialog(color)
	eq_(color, '#FF0000') #Red

if __name__ == "__main__":
	SelectRed_test()