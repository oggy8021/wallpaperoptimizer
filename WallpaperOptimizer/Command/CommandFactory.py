# -*- coding: utf-8 -*-

from WallpaperOptimizer.Command.Gnome2Command import Gnome2Command
from WallpaperOptimizer.Command.Gnome3Command import Gnome3Command

class CommandFactory(object):

	def _createCommand(self, windowmanager):
		if windowmanager == 'Gnome2':
			return Gnome2Command()
		elif windowmanager == 'Gnome3':
			return Gnome3Command() 

	def create(self, windowmanager):
		cmd = self._createCommand(windowmanager)
		return cmd
