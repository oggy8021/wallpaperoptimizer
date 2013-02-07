# -*- coding: utf-8 -*-

# module WallpaperOptimizer __init__.py
__all__=["Core","DesktopBase", "Applet","AppIndicator","Glade", "ChangerDir","Config","Options","OptionsBase","WorkSpace","Dist"]

import os.path
import xdg.BaseDirectory

USERENVDIR = os.path.join(xdg.BaseDirectory.save_data_path('wallpaperoptimizer'))
ICONDIR = "/usr/share/WallpaperOptimizer"
LIBRARYDIR = os.path.abspath(os.path.dirname(__file__))

if os.path.exists(USERENVDIR) == False:
        os.mkdir(USERENVDIR)
