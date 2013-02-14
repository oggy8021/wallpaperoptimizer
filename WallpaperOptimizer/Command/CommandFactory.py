# -*- coding: utf-8 -*-

from WallpaperOptimizer.Command.Gnome2Command import Gnome2Command
from WallpaperOptimizer.Command.Gnome3Command import Gnome3Command

class CommandFactory(object):

    def createCommand(self, gnomever):
        if gnomever == '2':
            return Gnome2Command()
        elif gnomever == '3':
            return Gnome3Command() 

    def create(self, gnomever):
        cmd = self.createCommand(gnomever)
        return cmd
