# -*- coding: utf-8 -*-

import subprocess

from WallpaperOptimizer.Command.Command import Command


class Xfce4Command(Command):
    def setWall(self, path):
        self.ret = subprocess.call(
            [self.command,
                "-c",
                "xfce4-desktop",
                "-p",
                "/backdrop/screen0/monitor0/image-path",
                "-t",
                "string",
                "-s",
                path]
        )
        return self.ret

    def setView(self):
        self.retopt = subprocess.call(
            [self.command,
                "-n",
                "-c",
                "xfce4-desktop",
                "-p",
                "/backdrop/screen0/xinarama-stretch",
                "-t",
                "boot",
                "-s",
                "true"]
        )
        return self.retopt

    def getWall(self):
        self.current = subprocess.Popen(
            [self.command,
                "-c",
                "xfce4-desktop",
                "-p",
                "/backdrop/screen0/monitor0/image-path"],
            stdout=subprocess.PIPE
        ).communicate()[0].rstrip()
        return self.current

    def __init__(self):
        self.command = "xfconf-query"
