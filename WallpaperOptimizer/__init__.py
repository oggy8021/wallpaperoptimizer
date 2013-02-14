# -*- coding: utf-8 -*-

# module WallpaperOptimizer __init__.py
__all__ = [
           "Core",
           "DesktopBase",
           "Applet",
           "AppIndicator",
           "Glade",
           "ChangerDir",
           "Config",
           "Options",
           "OptionsBase",
           "WorkSpace"
           ]

#! WorkSpaceに同関数
def _splitLines(self, string):
    ptn = re.compile('\n')
    return ptn.split(string)

def _verextract(string):
    ptn = re.compile('^.+(\d+).(\d+).(\d+).*$')
    (ver, rev1, rev2) = ptn.split(string)[1:4]
    return ver

VERSION = '0.7.0.0'
AUTHOR = 'oggy'

import os.path
import xdg.BaseDirectory

USERENVDIR = os.path.join(xdg.BaseDirectory.save_data_path('wallpaperoptimizer'))
ICONDIR = "/usr/share/WallpaperOptimizer"
LIBRARYDIR = os.path.abspath(os.path.dirname(__file__))

if os.path.exists(USERENVDIR) == False:
        os.mkdir(USERENVDIR)

import os.path
import subprocess
import re

gnomesessions='/usr/bin/gnome-session'
gnomeabout='/usr/bin/gnome-about'
if os.path.exists(gnomesessions):
    GNOMEVER = _verextract(subprocess.Popen([gnomesessions,'--version'], stdout=subprocess.PIPE).communicate()[0])
elif os.path.exists(gnomeabout):
    GNOMEVER = _verextract(_splitLines(subprocess.Popen([gnomeabout,'--gnome-version'], stdout=subprocess.PIPE).communicate()[0])[0])
