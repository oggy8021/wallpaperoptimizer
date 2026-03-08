# -*- coding: utf-8 -*-

import os.path
import harite.WallpaperOptimizer as WallpaperOptimizer

from harite.WallpaperOptimizer.Widget.SaveWallpaperDialog import SaveWallpaperDialog

#from nose.tools import ok_, eq_


def SaveWallpaper_test():
    gladefile = os.path.abspath(
        os.path.join(
            WallpaperOptimizer.LIBRARYDIR,
            'glade',
            'wallpositapplet.glade'))

    saveWallpaperDialog = SaveWallpaperDialog(gladefile)
    path = saveWallpaperDialog.openDialog()
    print path

if __name__ == "__main__":
    SaveWallpaper_test()
