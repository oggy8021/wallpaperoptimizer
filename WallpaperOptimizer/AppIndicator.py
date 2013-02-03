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

try:
    import gnome.ui
except:
    print 'not installed Python bindings for the GNOME desktop environment'
    print 'ex) sudo apt-get install python-gnome2'
    print 'ex) sudo yum install python-gnome2-gnome'
    sys.exit(2)

import appindicator
from distutils.sysconfig import PREFIX, get_python_lib

from WallpaperOptimizer.DesktopBase import DesktopBase
from WallpaperOptimizer.Core import Core
from WallpaperOptimizer.Glade import Glade
from WallpaperOptimizer.Widget.ErrorDialog import ErrorDialog
from WallpaperOptimizer.Widget.ImgOpenDialog import ImgOpenDialog
from WallpaperOptimizer.Widget.SettingDialog import SettingDialog
from WallpaperOptimizer.Widget.ColorSelectionDialog import ColorSelectionDialog
from WallpaperOptimizer.Widget.SaveWallpaperDialog import SaveWallpaperDialog


class AppIndicator(DesktopBase):

    def menu_setup(self):
        self.menu = gtk.Menu()

        self.visible_item = gtk.MenuItem("表示/非表示")
        self.preference_item = gtk.MenuItem("設定")
        self.color_item = gtk.MenuItem("色選択")
        self.about_item = gtk.MenuItem("情報")
        self.quit_item = gtk.MenuItem("終了")
#!    あとで揃える
        self.quit_item.connect("activate", self.escape1)
        self.quit_item.show()

        self.menu.append(self.quit_item)
        
    def __init__(self, option, logging):
        self.indicator = appindicator.Indicator('WallpaperOptimzier-indicator',
                                                "indicator-messages",
                                                appindicator.CATEGORY_APPLICATION_STATUS)
        self.option = option
        self.logging = logging

#      Initialize Status
        self.timeoutObject = None
        self.bVisible = True
        self.bCanceled = True
        self.bEntryPath = [False,False]

#      Initialize AppIndicator
        self.indicator.set_status(appindicator.STATUS_ACTIVE)
#! pngファイルに/glipperさん参考になるか
        self.indicator.set_attention_icon("indicator-messages-new")
        self.menu_setup()
        self.indicator.set_menu(self.menu)

# ここから下は、Applet.py l.456 "AppletOptions extends Options class"からに倣う
#        self.option = AppletOptions()
#!            →optionを渡せなかったので、アプレットにて用意していた。
#!            →今度は渡せる。ただし、初期値が違う可能性も
        self.core = Core(self.option)

#      Initialize Applet
#!        self.gladefile = os.path.abspath(
#!            os.path.join(get_python_lib(),'WallpaperOptimizer','glade','wallpositapplet.glade'))
        self.gladefile = os.path.abspath(
            os.path.join('.','WallpaperOptimizer','glade','wallpositapplet.glade'))
        self.walkTree = Glade(self.gladefile, "WallPosit_MainWindow")
        self.window = self.walkTree.get_widget("WallPosit_MainWindow")
#!        self.window.set_icon(self._select_icon(self.bCanceled))
#!        →違う制御になりそう
        self._linkGladeTree()
        if self.core.Ws.isSeparate():
            self.option.opts.combine = False
            self.radSeparate.set_active(True)
            self.radCombine.set_sensitive(False)
        self.btnSave.set_sensitive(False)
        self.btnSetWall.set_sensitive(False)
        if not self.core.config.lDisplay.getBool():
            self.btnDaemonize.set_sensitive(False)
        self.btnCancelDaemonize.set_sensitive(False)

#        self.cid_stat = self.statbar.get_context_id('status')
#!        →違う制御になりそう

#      bindCallbackFunction
        dic = {
#            "on_tglBtn_pressed" : self.tglBtn_pressed,
#            "on_tglBtn_toggled" : self.tglBtn_toggled,
#            "on_tglBtn_released" : self.tglBtn_released,
#            "on_spnMergin_value_changed" : self.spnMergin_value_changed,
#            "on_radFixed_toggled" : self.radFixed_toggled,
#            "on_radCombine_toggled" : self.radCombine_toggled,
#            "on_btnGetImg_clicked" : self.btnGetImg_clicked,
#            "on_entPath_insert_text" : self.entPath_insert,
#            "on_btnClrPath_clicked" : self.btnGetImg_clicked,
#            "on_btnSetting_clicked" : self.btnSetting_clicked,
#            "on_btnSetColor_clicked" : self.btnSetColor_clicked,
#            "on_btnSave_clicked" : self.btnSave_clicked,
#            "on_btnSetWall_clicked" : self.btnSetWall_clicked,
#            "on_spnInterval_value_changed" : self.spnInterval_value_changed,
#            "on_btnDaemonize_clicked" : self.btnDaemonize_clicked,
#            "on_btnCancelDaemonize_clicked" : self.btnCancelDaemonize_clicked,
#            "on_btnAbout_clicked" : self.btnAbout_clicked,
            "on_btnAbout_clicked" : self.escape1,
#            "on_WallPosit_MainWindow_delete_event" : self.btnWindowClose_clicked
            "on_WallPosit_MainWindow_delete_event" : self.escape2
            }
        self.walkTree.signal_autoconnect(dic)
#!        →繰り返し実行はまだ手をつけない
#      未実装ボタン
        self.btnHelp.set_sensitive(False)
#      View
#        self._writeStatusbar(self.statbar, self.cid_stat, 'Running ... applet mode.')
#!        →違う制御になりそう
#      記憶
        self.pos = self.window.get_position()

    def escape1(self, widget):
        sys.exit(0)

    def escape2(self, widget, hoge):
        sys.exit(0)

