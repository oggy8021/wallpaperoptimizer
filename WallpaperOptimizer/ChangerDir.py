# -*- coding: utf-8 -*-

import random
import sys, os, os.path, re

class ChangerDir(object):

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
		srcdir = os.path.expanduser(srcdir)
		files = os.listdir(srcdir)
		self.imgfiles = []
		for file in files:
			if (os.path.isfile(srcdir + file) and Ext.search(file)):
				self.imgfiles.append(os.path.abspath(srcdir + file))
		self.maxlen = len(self.imgfiles)

		if (self.maxlen < 1):
#			print 'Warning: %s に画像ファイルがありません' % srcdir
#			sys.exit(2)
			return False


if __name__ == "__main__":
	import sys
	wChg = ChangerDir(sys.argv[1])
	for i in range (0,int(sys.argv[2])):
		print i, wChg.getImgfileSeq()
	print '---'
	for i in range (0,int(sys.argv[2])):
		print i, wChg.getImgfileRnd()
