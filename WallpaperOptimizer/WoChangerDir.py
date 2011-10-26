# -*- coding: utf-8 -*-

import random
import os, os.path, re

class WoChangerDir(object):

	def getImgfileSeq(self):
		if (self.maxlen <= self.fp):
			self.fp = 0
		imgfile = self.imgfiles[self.fp]
		self.fp += 1
		return imgfile

	def getImgfileRnd(self):
		return self.imgfiles[int(random.randint(0,self.maxlen-1))]

	def __init__(self, srcdir='.'):
		self.fp = 0

		#http://www.python.jp/Zope/articles/tips/regex_howto/regex_howto_3 (sec 3.2)
		Ext = re.compile(r"\.(gif|jpe?g|bmp|png)$", re.IGNORECASE)
		files = os.listdir(srcdir)
		self.imgfiles = []
		for file in files:
			file
			if (os.path.isfile(srcdir + file) and Ext.search(file)):
				self.imgfiles.append(os.path.abspath(srcdir + file))
		self.maxlen = len(self.imgfiles)

if __name__ == "__main__":
	import sys
	wChg = WoChangerDir(sys.argv[1])
	for i in range (0,int(sys.argv[2])):
		print i, wChg.getImgfileSeq()
	print '---'
	for i in range (0,int(sys.argv[2])):
		print i, wChg.getImgfileRnd()
