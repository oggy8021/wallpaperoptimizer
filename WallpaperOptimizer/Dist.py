# -*- coding: utf-8 -*-

import platform

class Dist(object):

    def isRhel(self):
        return self.bRhel

    def isDebian(self):
        return self.bDebian
    
    def __init__(self):
        self.rhel = ('CentOS','Red Hat Linux') #Fedora, Rhel, Scentific, etc
        self.debian = ('Ubuntu') #Debian, Lubuntu, Xubuntu, etc

        self.bRhel = False
        self.bDebian = False

        self.dist = platform.linux_distribution()[0]
        if self.dist in self.rhel:
            self.bRhel = True
        elif self.dist in self.debian:
            self.bDebian = True
#
#if __name__ == "__main__":
#    dist = Dist()
#    print dist.isRhel()
#    print dist.isDebian()