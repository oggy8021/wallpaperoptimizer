# -*- coding: utf-8 -*-

import os.path

import WallpaperOptimizer

from WallpaperOptimizer.Widget.SettingDialog import SettingDialog

from nose.tools import eq_


def Setting_SetDefaultClickCancel_test():
    gladefile = os.path.abspath(
        os.path.join(
            WallpaperOptimizer.LIBRARYDIR,
            'glade',
            'wallpositapplet.glade'))
    lWidth = 0
    lHeight = 0
    rWidth = 0
    rHeight = 0
    lSrcdir = ''
    rSrcdir = ''

    settingDialog = SettingDialog(gladefile)
    settingArgs = settingDialog.openDialog(
        [lWidth, lHeight], [rWidth, rHeight], [lSrcdir, rSrcdir])
    eq_(settingArgs[0], False)


def Setting_SetDefaultClickOk_test():
    gladefile = os.path.abspath(
        os.path.join(
            WallpaperOptimizer.LIBRARYDIR,
            'glade',
            'wallpositapplet.glade'))
    lWidth = 0
    lHeight = 0
    rWidth = 0
    rHeight = 0
    lSrcdir = ''
    rSrcdir = ''

    settingDialog = SettingDialog(gladefile)
    settingArgs = settingDialog.openDialog(
        [lWidth, lHeight], [rWidth, rHeight], [lSrcdir, rSrcdir])

    eq_(settingArgs[0], (lWidth, lHeight))
    eq_(settingArgs[1], (rWidth, rHeight))
    eq_(settingArgs[2], (lSrcdir, rSrcdir))


def Setting_SetValueClickCancel_test():
    gladefile = os.path.abspath(
        os.path.join(
            WallpaperOptimizer.LIBRARYDIR,
            'glade',
            'wallpositapplet.glade'))
    lWidth = 1920
    lHeight = 1280
    rWidth = 1280
    rHeight = 1024
    lSrcdir = '/home/katsu/Wallpaper/1920'
    rSrcdir = '/home/katsu/Wallpaper/1280'

    settingDialog = SettingDialog(gladefile)
    settingArgs = settingDialog.openDialog(
        [lWidth, lHeight], [rWidth, rHeight], [lSrcdir, rSrcdir])

    eq_(settingArgs[0], False)


def Setting_SetValueClickOk_test():
    gladefile = os.path.abspath(
        os.path.join(
            WallpaperOptimizer.LIBRARYDIR,
            'glade',
            'wallpositapplet.glade'))
    lWidth = 1920
    lHeight = 1280
    rWidth = 1280
    rHeight = 1024
    lSrcdir = '/home/katsu/Wallpaper/1920'
    rSrcdir = '/home/katsu/Wallpaper/1280'

    settingDialog = SettingDialog(gladefile)
    settingArgs = settingDialog.openDialog(
        [lWidth, lHeight], [rWidth, rHeight], [lSrcdir, rSrcdir])

    eq_(settingArgs[0], (lWidth, lHeight))
    eq_(settingArgs[1], (rWidth, rHeight))
    eq_(settingArgs[2], (lSrcdir, rSrcdir))


def Setting_LeftValueDefaultClickOk_test():
    gladefile = os.path.abspath(
        os.path.join(
            WallpaperOptimizer.LIBRARYDIR,
            'glade',
            'wallpositapplet.glade'))
    lWidth = 0
    lHeight = 0
    rWidth = 1280
    rHeight = 1024
    lSrcdir = '/home/katsu/Wallpaper/1920'
    rSrcdir = '/home/katsu/Wallpaper/1280'

    settingDialog = SettingDialog(gladefile)
    settingArgs = settingDialog.openDialog(
        [lWidth, lHeight], [rWidth, rHeight], [lSrcdir, rSrcdir])

    eq_(settingArgs[0], (lWidth, lHeight))
    eq_(settingArgs[1], (rWidth, rHeight))
    eq_(settingArgs[2], (lSrcdir, rSrcdir))


def Setting_RightValueDefaultClickOk_test():
    gladefile = os.path.abspath(
        os.path.join(
            WallpaperOptimizer.LIBRARYDIR,
            'glade',
            'wallpositapplet.glade'))
    lWidth = 1920
    lHeight = 1280
    rWidth = 0
    rHeight = 0
    lSrcdir = '/home/katsu/Wallpaper/1920'
    rSrcdir = '/home/katsu/Wallpaper/1280'

    settingDialog = SettingDialog(gladefile)
    settingArgs = settingDialog.openDialog(
        [lWidth, lHeight], [rWidth, rHeight], [lSrcdir, rSrcdir])

    eq_(settingArgs[0], (lWidth, lHeight))
    eq_(settingArgs[1], (rWidth, rHeight))
    eq_(settingArgs[2], (lSrcdir, rSrcdir))


def Setting_lSrcdirValueDefaultClickOk_test():
    gladefile = os.path.abspath(
        os.path.join(
            WallpaperOptimizer.LIBRARYDIR,
            'glade',
            'wallpositapplet.glade'))
    lWidth = 1920
    lHeight = 1280
    rWidth = 1280
    rHeight = 1024
    lSrcdir = ''
    rSrcdir = '/home/katsu/Wallpaper/1280'

    settingDialog = SettingDialog(gladefile)
    settingArgs = settingDialog.openDialog(
        [lWidth, lHeight], [rWidth, rHeight], [lSrcdir, rSrcdir])

    eq_(settingArgs[0], (lWidth, lHeight))
    eq_(settingArgs[1], (rWidth, rHeight))
    eq_(settingArgs[2], ('', '/home/katsu/Wallpaper/1280'))


def Setting_rSrcdirValueDefaultClickOk_test():
    gladefile = os.path.abspath(
        os.path.join(
            WallpaperOptimizer.LIBRARYDIR,
            'glade',
            'wallpositapplet.glade'))
    lWidth = 1920
    lHeight = 1280
    rWidth = 1280
    rHeight = 1024
    lSrcdir = '/home/katsu/Wallpaper/1920'
    rSrcdir = ''

    settingDialog = SettingDialog(gladefile)
    settingArgs = settingDialog.openDialog(
        [lWidth, lHeight], [rWidth, rHeight], [lSrcdir, rSrcdir])

    eq_(settingArgs[0], (lWidth, lHeight))
    eq_(settingArgs[1], (rWidth, rHeight))
    eq_(settingArgs[2], ('/home/katsu/Wallpaper/1920', ''))
