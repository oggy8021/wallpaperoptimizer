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

import WallpaperOptimizer
from WallpaperOptimizer.DesktopBase import DesktopBase
from WallpaperOptimizer.Core import Core
from WallpaperOptimizer.Glade import Glade
from WallpaperOptimizer.Widget.ErrorDialog import ErrorDialog
from WallpaperOptimizer.Widget.ImgOpenDialog import ImgOpenDialog
from WallpaperOptimizer.Widget.SettingDialog import SettingDialog
from WallpaperOptimizer.Widget.ColorSelectionDialog import ColorSelectionDialog
from WallpaperOptimizer.Widget.SaveWallpaperDialog import SaveWallpaperDialog

class AppIndicator(DesktopBase):

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

        print "AppIndicator.py " + self.indicator.get_icon_theme_path()
        self.indicator.set_icon('wallopt')
 
#      optionInitialize
        self.option.opts.window = True
        self.option.args = ['','']
        self.core = Core(self.option)

#      Initialize Applet
        self.gladefile = os.path.abspath(
            os.path.join(WallpaperOptimizer.LIBRARYDIR,'glade','wallpositapplet.glade'))
        self.walkTree = Glade(self.gladefile, "WallPosit_MainWindow")
        self.window = self.walkTree.get_widget("WallPosit_MainWindow")
        self.window.set_icon(self._select_icon(self.bCanceled))
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

        self.cid_stat = self.statbar.get_context_id('status')

#      bindCallbackFunction
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
#      未実装ボタン
        self.btnHelp.set_sensitive(False)
#      View
        self._writeStatusbar(self.statbar, self.cid_stat, 'Running ... applet mode.')
#      記憶
        self.pos = self.window.get_position()

