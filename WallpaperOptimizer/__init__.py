# -*- coding: utf-8 -*-

# module WallpaperOptimizer __init__.py
__all__=["Core","DesktopBase", "Applet","AppIndicator","Glade", "ChangerDir","Config","Options","OptionsBase","WorkSpace"]

import os.path
import xdg.BaseDirectory

USERENVDIR = os.path.join(xdg.BaseDirectory.save_data_path('wallpaperoptimizer'))
ICONDIR = "/usr/share/WallpaperOptimizer"
LIBRARYDIR = os.path.abspath(os.path.dirname(__file__))

if os.path.exists(USERENVDIR) == False:
        os.mkdir(USERENVDIR)


import platform

RHELGROUP = ('CentOS','Red Hat Linux') #Fedora, Rhel, Scentific, etc
DEBIANGROUP = ('Ubuntu') #Debian, Lubuntu, Xubuntu, etc

bRhel = False
bDebian = False

dist = platform.linux_distribution()[0]
if dist in RHELGROUP:
    bRhel = True 
elif dist in DEBIANGROUP:
    bDebian = True

def isRhel():
    return bRhel

def isDebian():
    return bDebian
