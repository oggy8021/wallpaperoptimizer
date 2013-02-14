# -*- coding: utf-8 -*-

""" WallpaperOptimizer::AppIndicator

wallpaperoptimizer AppIndicator module.
"""

import sys
import os.path
import pygtk
pygtk.require("2.0")
import gtk
try:
    import glib as glibobj
#    Ubuntuでは活きた
except:
    try:
        import gobject as glibobj
    except:
        sys.exit(2)

import appindicator

import WallpaperOptimizer

from WallpaperOptimizer.WindowBase import WindowBase
from WallpaperOptimizer.Core import Core
#!from WallpaperOptimizer.Glade import Glade
from WallpaperOptimizer.Widget.ErrorDialog import ErrorDialog
from WallpaperOptimizer.Widget.ImgOpenDialog import ImgOpenDialog
from WallpaperOptimizer.Widget.SettingDialog import SettingDialog
from WallpaperOptimizer.Widget.ColorSelectionDialog import ColorSelectionDialog
from WallpaperOptimizer.Widget.SaveWallpaperDialog import SaveWallpaperDialog

class AppIndicator(WindowBase):

    def quit(self, widget):
        sys.exit(0)

    def _create_menu(self):
        self.indicatormenu = gtk.Menu()

        self.visible_item = gtk.MenuItem("表示/非表示")
        self.preference_item = gtk.MenuItem("設定")
        self.color_item = gtk.MenuItem("色選択")
        self.about_item = gtk.MenuItem("情報")
        self.quit_item = gtk.MenuItem("終了")

        self.visible_item.connect("activate", self._visibleCtrl)
        self.preference_item.connect("activate", self._preferences)
        self.color_item.connect("activate", self._selectColor)
        self.about_item.connect("activate", self._about)
        self.quit_item.connect("activate", self.quit)

        self.visible_item.show()
        self.preference_item.show()
        self.color_item.show()
        self.about_item.show()
        self.quit_item.show()

        self.indicatormenu.append(self.visible_item)
        self.indicatormenu.append(self.preference_item)
        self.indicatormenu.append(self.color_item)
        self.indicatormenu.append(self.about_item)
        self.indicatormenu.append(self.quit_item)

    def btnDaemonize_clicked(self, widget):
        self.window.hide()
        self.window.set_icon(self._select_icon(self.bCanceled))
        self.bCanceled = False
        self.bVisible = False
        self.indicator.set_icon('wallopt')
        self._switchWidget(False)
        self._presetCore()
        self.timeoutObject = glibobj.timeout_add(self.option.opts.interval*1000
                , self._timeout, self)
        self.logging.debug('%20s' % 
                'Start Daemonize ... interval [%d].' % self.option.opts.interval)
        self._runChanger()

    def btnCancelDaemonize_clicked(self, widget):
        self.bCanceled = True
        self.indicator.set_icon('wallopt_off')
        self.window.set_icon(self._select_icon(self.bCanceled))
        glibobj.source_remove(self.timeoutObject)
        self.timeoutObject = None
        self._writeStatusbar(self.statbar, self.cid_stat, 'Cancel ... changer action.')
        self._switchWidget(True)

    def _select_icon(self,bCanceled):
        if bCanceled:
            icon = self.dis_icon
        else:
            icon = self.ena_icon
        return icon

    def _loadIcon(self):
        self.dis_icon = gtk.gdk.pixbuf_new_from_file(os.path.abspath(
                os.path.join(self.indicator.get_icon_theme_path(),'wallopt_off.png')))
        self.ena_icon = gtk.gdk.pixbuf_new_from_file(os.path.abspath(
                os.path.join(self.indicator.get_icon_theme_path(),'wallopt.png')))
        
    def __init__(self, option, logging):
#        id, icon_name, category, icon_theme_path
        self.indicator = appindicator.Indicator('WallpaperOptimzier',
                                                "wallopt_off",
                                                appindicator.CATEGORY_APPLICATION_STATUS,
                                                WallpaperOptimizer.ICONDIR)
        self.option = option
        self.logging = logging

#      Initialize Status
        self.timeoutObject = None
        self.bVisible = True
        self.bCanceled = True
        self.bEntryPath = [False,False]

#      Initialize AppIndicator
        self._loadIcon()
        self.indicator.set_status(appindicator.STATUS_ACTIVE)
        self._create_menu()
        self.indicator.set_menu(self.indicatormenu)
        gtk.window_set_default_icon(self._select_icon(self.bCanceled))

        self.indicator.set_icon('wallopt')
 
#      optionInitialize
        self.option.opts.window = True
        self.option.args = ['','']
        self.core = Core(self.option)

#      Initialize Applet
        self._initializeWindow()

