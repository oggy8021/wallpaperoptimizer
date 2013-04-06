# -*- coding: utf-8 -*-

# module WallpaperOptimizer __init__.py
__all__ = [
			"Core",
			"WindowBase",
			"Applet",
			"AppIndicator",
			"Glade",
			"ChangerDir",
			"Config",
			"Options",
			"OptionsBase",
			"WorkSpace",
			"Starter",
			"StarterFactory",
			"Gnome2Starter",
			"Gnome3Starter"
			]

def _verextract(string):
	ptn = re.compile('^.+(\d+).(\d+).(\d+).*$')
	(ver, rev1, rev2) = ptn.split(string)[1:4]
	return ver

def _wmextract(string):
	ptn = re.compile('^_NET_WM_NAME\(UTF8_STRING\)\s+=\s+"(.+)"\s+$')
	wm_name = ptn.split(string)[1]
	return wm_name

VERSION = '0.8.0.0'
AUTHOR = 'oggy <oggyist@gmail.com>'

import os.path
import xdg.BaseDirectory

USERENVDIR = os.path.join(xdg.BaseDirectory.save_data_path('wallpaperoptimizer'))
ICONDIR = "/usr/share/WallpaperOptimizer"
LIBRARYDIR = os.path.abspath(os.path.dirname(__file__))

if os.path.exists(USERENVDIR) == False:
		os.mkdir(USERENVDIR)

import sys
import os.path
import subprocess
import re

xprop='/usr/bin/xprop'
if os.path.exists(xprop):
	window_id = (subprocess.Popen([xprop, '-root', '_NET_SUPPORTING_WM_CHECK'], stdout=subprocess.PIPE).communicate()[0]).split(' ')[4]
	wm_name = _wmextract(subprocess.Popen([xprop, '-id', window_id, '8s', '_NET_WM_NAME'], stdout=subprocess.PIPE).communicate()[0])

WINDOWMANAGER = 'Gnome'
if wm_name == 'Xfwm4':
	WINDOWMANAGER="xfce4"
elif wm_name == 'Openbox':
	WINDOWMANAGER="lxde"
else:
	# Metacity, Compiz, GNOME Shell
	gnomesessions='/usr/bin/gnome-session'
	if os.path.exists(gnomesessions):
		GNOMEVER = _verextract(subprocess.Popen([gnomesessions,'--version'], stdout=subprocess.PIPE).communicate()[0])
		WINDOWMANAGER = WINDOWMANAGER + GNOMEVER