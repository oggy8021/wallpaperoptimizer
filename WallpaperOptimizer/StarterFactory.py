# -*- coding: utf-8 -*-

from harite.WallpaperOptimizer.Gnome2Starter import Gnome2Starter
from harite.WallpaperOptimizer.Gnome3Starter import Gnome3Starter


class StarterFactory(object):
    def _createStarter(self, windowmanager):
        if windowmanager == 'Gnome2':
            return Gnome2Starter()
        elif (
            windowmanager == 'Gnome3' or
            windowmanager == 'xfce40' or
            windowmanager == 'xfce41' or
            windowmanager == 'lxde'
        ):
            return Gnome3Starter()

    def create(self, windowmanager):
        starter = self._createStarter(windowmanager)
        return starter
