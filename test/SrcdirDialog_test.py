# -*- coding: utf-8 -*-

import os.path
import WallpaperOptimizer

from WallpaperOptimizer.Widget.SrcdirDialog import SrcdirDialog

from nose.tools import eq_


def SrcdirDialogSetNullDir_test():
    gladefile = os.path.abspath(
        os.path.join(
            WallpaperOptimizer.LIBRARYDIR,
            'glade',
            'wallpositapplet.glade'))
    dir = ''
    addlr = u'左'

    srcdirDialog = SrcdirDialog(gladefile)
    dir = srcdirDialog.openDialog(dir, addlr)
    assert(dir != '')


def SrcdirDialogSetDir_test():
    gladefile = os.path.abspath(
        os.path.join(
            WallpaperOptimizer.LIBRARYDIR,
            'glade',
            'wallpositapplet.glade'))
    dir1 = '/home/katsu/Wallpaper/1920'
    addlr = u'右'

    srcdirDialog = SrcdirDialog(gladefile)
    dir2 = srcdirDialog.openDialog(dir1, addlr)
    eq_(dir2, dir1)

if __name__ == "__main__":
    SrcdirDialogSetNullDir_test()
    SrcdirDialogSetDir_test()
