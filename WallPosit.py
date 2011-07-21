#!/usr/bin/env python

#coding: UTF-8

import sys

import ImgFile
from debuggy import debugCon



#///////////////////////////////////////////////////////////////////////////////////// main

fileA = sys.argv[1]
fileB = sys.argv[2]

imgA = ImgFile.ImgFile(fileA)
imgB = ImgFile.ImgFile(fileB)

imgA.setGeometry()
imgB.setGeometry()

debugCon(imgA.x)
debugCon(imgA.y)
debugCon(imgB.x)
debugCon(imgB.y)
