#!/usr/bin/env python

#coding: UTF-8

import sys

import ImageFile
import debuggy



#///////////////////////////////////////////////////////////////////////////////////// main

fileA = sys.argv[1]
fileB = sys.argv[2]

imgA = ImgFile(fileA)
imgB = ImgFile(fileB)

debuggy.debugCon(imgA.x)
debuggy.debugCon(imgA.y)
debuggy.debugCon(imgB.x)
debuggy.debugCon(imgB.y)

