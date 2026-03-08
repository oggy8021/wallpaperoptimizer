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
    net_wm_name = ptn.split(string)[1]
    return net_wm_name


def _xfceextract(string):
    ptn = re.compile('^.+\s(\d+).(\d+).(\d+)\s.*$')
    (ver, rev1, rev2) = ptn.split(string)[1:4]
    return rev2

VERSION = '0.9.0.0'
AUTHOR = 'oggy <oggyist@gmail.com>'


import os.path

# xdg may not be available in test environments (Windows); fall back to
# a user-home based path when it's missing.
try:
    import xdg.BaseDirectory as _xdg
    USERENVDIR = os.path.join(_xdg.save_data_path('wallpaperoptimizer'))
except Exception:
    USERENVDIR = os.path.join(os.path.expanduser('~'), '.wallpaperoptimizer')
ICONDIR = "/usr/share/WallpaperOptimizer"
LIBRARYDIR = os.path.abspath(os.path.dirname(__file__))

if os.path.exists(USERENVDIR) is False:
        os.mkdir(USERENVDIR)

import subprocess
import re

try:
    xprop = '/usr/bin/xprop'
    wm_name = ''
    if os.path.exists(xprop):
        window_id = (
            subprocess.Popen(
                [xprop,
                 '-root',
                 '_NET_SUPPORTING_WM_CHECK'],
                stdout=subprocess.PIPE).communicate()[0]
            ).split(' ')[4]
        wm_name = _wmextract(
            subprocess.Popen(
                [xprop,
                 '-id',
                 window_id,
                 '8s',
                 '_NET_WM_NAME'],
                stdout=subprocess.PIPE).communicate()[0])

    WINDOWMANAGER = 'Gnome'
    if wm_name == 'Xfwm4':
        WINDOWMANAGER = "xfce4"
        xfce4sessions = '/usr/bin/xfce4-session'
        if os.path.exists(xfce4sessions):
            XFCESUBREV = _xfceextract(
                subprocess.Popen(
                    [xfce4sessions, '--version'],
                    stdout=subprocess.PIPE
                ).communicate()[0].rstrip().splitlines()[0])
            WINDOWMANAGER = WINDOWMANAGER + XFCESUBREV
    elif wm_name == 'Openbox':
        WINDOWMANAGER = "lxde"
    else:
        # Metacity, Compiz, GNOME Shell
        gnomesessions = '/usr/bin/gnome-session'
        if os.path.exists(gnomesessions):
            GNOMEVER = _verextract(
                subprocess.Popen(
                    [gnomesessions, '--version'],
                    stdout=subprocess.PIPE
                ).communicate()[0])
            WINDOWMANAGER = WINDOWMANAGER + GNOMEVER
except Exception:
    # In non-Linux or headless test environments, keep sensible defaults
    WINDOWMANAGER = 'Gnome'
