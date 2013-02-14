# -*- coding: utf-8 -*-

from WallpaperOptimizer.Gnome2Starter import Gnome2Starter
from WallpaperOptimizer.Gnome3Starter import Gnome3Starter

class StarterFactory(object):

    def _createStarter(self, gnomever):
        if gnomever == '2':
            return Gnome2Starter()
        elif gnomever == '3':
            return Gnome3Starter()

    def create(self, gnomever):
        starter = self._createStarter(gnomever)
        return starter