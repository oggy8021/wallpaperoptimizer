# -*- coding: utf-8 -*-

import sys
import os.path

import gtk
try:
    import glib as glibobj
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

from WallpaperOptimizer.Glade import Glade
from WallpaperOptimizer.Widget.ErrorDialog import ErrorDialog
from WallpaperOptimizer.Widget.ImgOpenDialog import ImgOpenDialog
from WallpaperOptimizer.Widget.SettingDialog import SettingDialog
from WallpaperOptimizer.Widget.ColorSelectionDialog import ColorSelectionDialog
from WallpaperOptimizer.Widget.SaveWallpaperDialog import SaveWallpaperDialog

class DesktopBase(object):

    tgldic = dict()
    tgldic['tglPushLeftL'] = 'tglPushRightL'
    tgldic['tglPushRightL'] = 'tglPushLeftL'
    tgldic['tglUpperL'] = 'tglLowerL'
    tgldic['tglLowerL'] = 'tglUpperL'
    tgldic['tglPushLeftR'] = 'tglPushRightR'
    tgldic['tglPushRightR'] = 'tglPushLeftR'
    tgldic['tglUpperR'] = 'tglLowerR'
    tgldic['tglLowerR'] = 'tglUpperR'

    def _runErrorDialog(self, msg):
        errorDialog = ErrorDialog(self.gladefile)
        errorDialog.openDialog(msg)

    def _writeStatusbar(self, bar, cid, msg):
        bar.push(cid, msg)

    def _eraseStatusbar(self, bar, cid):
        bar.pop(cid)

#button group
    def tglBtn_pressed(self, widget):
        vsName = DesktopBase.tgldic[widget.get_name()]
        if (self.walkTree.get_widget(vsName).get_active()):
            self.walkTree.get_widget(vsName).set_active(False)

    def _setOptionValueFromBtn(self, btnName, lr, val=None):
        if (btnName.find('PushLeft') > 0 or btnName.find('PushRight') > 0):
            if val == None:
                val = 'center'
            self.option.opts.align[lr] = val
        elif (btnName.find('Upper') > 0 or btnName.find('Lower') > 0):
            if val == None:
                val = 'middle'
            self.option.opts.valign[lr] = val

    def tglBtn_toggled(self, widget):
        if widget.get_active():
            wName = widget.get_name()
            if wName.find('PushLeft') > 0:
                val = 'left'
            elif wName.find('PushRight') > 0:
                val = 'right'
            elif wName.find('Upper') > 0:
                val = 'top'
            elif wName.find('Lower') > 0:
                val = 'bottom'
            self._setOptionValueFromBtn(wName, widget.posit.idx, val)

    def tglBtn_released(self, widget):
        wName = widget.get_name()
        vsName = DesktopBase.tgldic[wName]
        if (widget.get_active() == False and 
                self.walkTree.get_widget(vsName).get_active() == False):
            self._setOptionValueFromBtn(wName, widget.posit.idx)


    def spnMergin_value_changed(self, widget):
        wName = widget.get_name()
        if wName.find('LMergin') > 0:
            idx = 0
        elif wName.find('RMergin') > 0:
            idx = 1
        elif wName.find('TopMergin') > 0:
            idx = 2
        elif wName.find('BtmMergin') > 0:
            idx = 3
        self.option.opts.mergin[idx] = int(self.walkTree.get_widget(wName).get_value_as_int())

    def radFixed_toggled(self, widget):
        if widget.get_name() == 'radFixed':
            self.option.opts.fixed = self.walkTree.get_widget(widget.get_name()).get_active()

    def radCombine_toggled(self, widget):
        if widget.get_name() == 'radCombine':
            self.option.opts.combine = self.walkTree.get_widget(widget.get_name()).get_active()

    def btnGetImg_clicked(self, widget):
        if widget.posit.idx == 0:
            entPath = self.entPathL
        else:
            entPath = self.entPathR
        if widget.get_name().find('Clr') > 0:
            path = ''
        else:
            imgopenDialog = ImgOpenDialog(self.gladefile)
            path = imgopenDialog.openDialog(self.core.option.args[widget.posit.idx], widget.posit.Kanji)
        if path <> False:
            self.core.option.args[widget.posit.idx] = path
            entPath.set_text(os.path.basename(path))

    def entPath_insert(self, widget, text, length, pos):
        if length > 0:
            self.bEntryPath[widget.posit.idx] = True
        else:
            self.bEntryPath[widget.posit.idx] = False
        if self.bEntryPath == [True, True]:
            self.btnSave.set_sensitive(True)
        elif self.bEntryPath == [True, False] or self.bEntryPath == [False, True]:
            self.btnSetWall.set_sensitive(True)
        else:
            self.btnSetWall.set_sensitive(False)

    def btnSetting_clicked(self, widget):
        settingDialog = SettingDialog(self.gladefile)
        settingArgs = settingDialog.openDialog([
                    self.core.config.lDisplay.width
                    , self.core.config.lDisplay.height
                    ],[
                    self.core.config.rDisplay.width
                    , self.core.config.rDisplay.height
                    ],[
                    self.core.config.lDisplay.srcdir
                    , self.core.config.rDisplay.srcdir
                    ])
        if not settingArgs == (False, False, False):
            for lr in (0,1):
                if lr == 0:
                    display = self.core.config.lDisplay
                    displaysize = settingArgs[0] #lDisplaySize
                else:
                    display = self.core.config.rDisplay
                    displaysize = settingArgs[1] #rDisplaySize
                for wh in (0,1):
                    display.setWidth(displaysize[wh])
                    display.setHeight(displaysize[wh])
                display.setSrcdir(settingArgs[2][lr])
            self.core.config.lDisplay.checkBool()
            self.core.config.rDisplay.checkBool()
            if self.core.config.lDisplay.getBool():
                self.btnDaemonize.set_sensitive(True)
            else:
                self.btnDaemonize.set_sensitive(False)
        else:
            pass

    def btnSetColor_clicked(self, widget):
        colorselectionDialog = ColorSelectionDialog(self.gladefile)
        self.option.opts.bgcolor = colorselectionDialog.openDialog(self.option.opts.bgcolor)

    def btnSave_clicked(self, widget):
        savewallpaperDialog = SaveWallpaperDialog(self.gladefile)
        self.core.option.opts.save = savewallpaperDialog.openDialog()
        if self.core.option.getSavePath() <> None:
            self._presetCore()
            try:
                self.core.singlerun()
            except self.core.CoreRuntimeError, msg:
                self.logger.error('** CoreRuntimeError: %s. ' % msg.value)
                self._runErrorDialog(self, '** CoreRuntimeError: %s. ' % msg.value)
        else:
            pass

    def btnSetWall_clicked(self, widget):
        self._presetCore()
        self.core.option.opts.setWall = True
        try:
            self.core.singlerun()
        except self.core.CoreRuntimeError, msg:
            self.logging.error('** CoreRuntimeError: %s. ' % msg.value)
            self._runErrorDialog(self, '** CoreRuntimeError: %s. ' % msg.value)

    def spnInterval_value_changed(self, widget):
        self.option.opts.interval = self.spnInterval.get_value_as_int()
        self._eraseStatusbar(self.statbar, self.cid_stat)
        self._writeStatusbar(self.statbar
                , self.cid_stat
                , 'Change Interval ... %d sec.' % self.option.opts.interval)

    def _runChanger(self):
        try:
            self.core.timerRun()
        except self.core.CoreRuntimeError, msg:
            self.logging.error('** CoreRuntimeError: %s. ' % msg.value)
            self._runErrorDialog(self, '** CoreRuntimeError: %s. ' % msg.value)

    def _timeout(self, applet):
        self.logging.debug('%20s at %d sec.' % ('Timeout', self.option.opts.interval))
        self._eraseStatusbar(self.statbar, self.cid_stat)
        self._writeStatusbar(self.statbar
                , self.cid_stat
                , 'Timeout ... run changer.')
        self._runChanger()
        if self.bCanceled:
            return False
        else:
            return True

    def btnDaemonize_clicked(self, widget):
        pass

    def btnCancelDaemonize_clicked(self, widget):
        pass

    def btnAbout_clicked(self, widget):
        icon = self._select_icon(self.bCanceled)
        about = gnome.ui.About("WallpaperOptimizer"
                            ,"0.6.0.0"    #version
                            ,"GPLv3"        #copyright
                            ,"wallpaperoptimizer is multi wallpaper changer."    #comments
                            ,["oggy"]        #**authors
                            ,["oggy"]        #**documenters
                            ,"oggy"        #*translator_credits
                            ,icon)            #gtk.gdk.Pixbuf
        about.show_all()

    def btnWindowClose_clicked(self, widget, event):
        self.bVisible = False
        self.pos = self.window.get_position()
        return widget.hide_on_delete()

    def _linkGladeTree(self):
        self.tglPushLeftL = self.walkTree.addPos('tglPushLeftL')
        self.tglPushRightL = self.walkTree.addPos('tglPushRightL')
        self.tglUpperL = self.walkTree.addPos('tglUpperL')
        self.tglLowerL = self.walkTree.addPos('tglLowerL')
        self.btnGetImgL = self.walkTree.addPos('btnGetImgL', True)
        self.entPathL = self.walkTree.addPos('entPathL')
        self.btnClrPathL = self.walkTree.addPos('btnClrPathL')
#
        self.tglPushLeftR = self.walkTree.addPos('tglPushLeftR')
        self.tglPushRightR = self.walkTree.addPos('tglPushRightR')
        self.tglUpperR = self.walkTree.addPos('tglUpperR')
        self.tglLowerR = self.walkTree.addPos('tglLowerR')
        self.btnGetImgR = self.walkTree.addPos('btnGetImgR', True)
        self.entPathR = self.walkTree.addPos('entPathR')
        self.btnClrPathR = self.walkTree.addPos('btnClrPathR')
#
        self.spnLMergin = self.walkTree.get_widget('spnLMergin')
        self.spnRMergin = self.walkTree.get_widget('spnRMergin')
        self.spnTopMergin = self.walkTree.get_widget('spnTopMergin')
        self.spnBtmMergin = self.walkTree.get_widget('spnBtmMergin')
        self.radCombine = self.walkTree.get_widget('radCombine')
        self.radSeparate = self.walkTree.get_widget('radSeparate')
        self.radFixed = self.walkTree.get_widget('radFixed')
        self.radNoFixed = self.walkTree.get_widget('radNoFixed')
#
        self.btnSetting = self.walkTree.get_widget('btnSetting')
        self.btnSetColor = self.walkTree.get_widget('btnSetColor')
        self.btnSave = self.walkTree.get_widget('btnSave')
        self.btnSetWall = self.walkTree.get_widget('btnSetWall')
        self.spnInterval = self.walkTree.get_widget('spnInterval')
        self.btnDaemonize = self.walkTree.get_widget('btnDaemonize')
        self.btnCancelDaemonize = self.walkTree.get_widget('btnCancelDaemonize')
        self.btnHelp = self.walkTree.get_widget('btnHelp')
        self.btnAbout = self.walkTree.get_widget('btnAbout')
        self.statbar = self.walkTree.get_widget('statusbar')

    def _presetCore(self):
        self.core.Ws.compareToScreen()
        self.core.Ws.setAttrScreenType()

    def _switchWidget(self, boolean):
        self.tglPushLeftL.set_sensitive(boolean)
        self.tglPushRightL.set_sensitive(boolean)
        self.tglUpperL.set_sensitive(boolean)
        self.tglLowerL.set_sensitive(boolean)
        self.btnGetImgL.set_sensitive(boolean)
        self.entPathL.set_sensitive(boolean)
        self.tglPushLeftR.set_sensitive(boolean)
        self.tglPushRightR.set_sensitive(boolean)
        self.tglUpperR.set_sensitive(boolean)
        self.tglLowerR.set_sensitive(boolean)
        self.btnGetImgR.set_sensitive(boolean)
        self.entPathR.set_sensitive(boolean)
        self.spnLMergin.set_sensitive(boolean)
        self.spnRMergin.set_sensitive(boolean)
        self.spnTopMergin.set_sensitive(boolean)
        self.spnBtmMergin.set_sensitive(boolean)
        self.radFixed.set_sensitive(boolean)
        self.radNoFixed.set_sensitive(boolean)
        self.btnSetting.set_sensitive(boolean)
        self.btnSetColor.set_sensitive(boolean)
        self.btnSave.set_sensitive(boolean)
        self.btnSetWall.set_sensitive(boolean)
        self.spnInterval.set_sensitive(boolean)
        self.btnDaemonize.set_sensitive(boolean)
        if boolean:
            self.btnCancelDaemonize.set_sensitive(False)
        else:
            self.btnCancelDaemonize.set_sensitive(True)
        if not self.core.Ws.isSeparate():
            self.radCombine.set_sensitive(boolean)
        self.radSeparate.set_sensitive(boolean)
#      未実装ボタン
#        self.btnHelp.set_sensitive(boolean)

    def _select_icon(self, bCanceled):
        pass

    def _visibleCtrl(self, *arguments):
        if self.bVisible:
            self.window.hide()
            self.bVisible = False
        else:
            self.window.move(self.pos[0], self.pos[1])
            self.window.show_all()
            self.bVisible = True

    def _preferences(self, *arguments):
        self.btnSetting_clicked(None)

    def _selectColor(self, *arguments):
        self.btnSetColor_clicked(None)

    def _about(self, *arguments):
        self.btnAbout_clicked(None)

    def _create_menu(self):
        pass

    def _setMenu(self):
        pass

    def _setPanelButton(self):
        pass

    def _setMenu(self):
        pass

    def _loadIcon(self):
        pass
    