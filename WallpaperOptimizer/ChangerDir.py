# -*- coding: utf-8 -*-

import os
import os.path
import re
import random

class ChangerDir(object):

	class FileCountZeroError(Exception):
		def __init__(self, value):
			self.value = value
		def __str__(self):
			return repr(self.value)

	def getImgfileSeq(self):
		if (self.maxlen <= self.fIdx):
			self.fIdx = 0
		imgfile = self.imgfiles[self.fIdx]
		self.fIdx += 1
		return imgfile

	def getImgfileRnd(self):
		return self.imgfiles[int(random.randint(0,self.maxlen-1))]

	def __init__(self, srcdir='.'):
		self.fIdx = 0

		#http://www.python.jp/Zope/articles/tips/regex_howto/regex_howto_3 (sec 3.2)
		Ext = re.compile(r"\.(gif|jpg|jpeg|bmp|png)$", re.IGNORECASE)
		srcdir = os.path.abspath(os.path.expanduser(srcdir))
		files = os.listdir(srcdir)
		self.imgfiles = []
		for file in files:
			if (os.path.isfile(srcdir + '/' + file) and Ext.search(file)):
				self.imgfiles.append(os.path.abspath(srcdir + '/' + file))
		self.maxlen = len(self.imgfiles)

		if (self.maxlen == 0):
			raise ChangerDir.FileCountZeroError('Directory does not have Imgfile [%s]' % srcdir)

if __name__ == "__main__":
	import sys
	wChg = ChangerDir(sys.argv[1])
	for i in range (0,int(sys.argv[2])):
		print i, wChg.getImgfileSeq()
	print '---'
	for i in range (0,int(sys.argv[2])):
		print i, wChg.getImgfileRnd()
