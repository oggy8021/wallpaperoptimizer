# -*- coding: utf-8 -*-

from getopt import getopt, GetoptError
import sys

class WoOption(object):

	def __init__(self):
		self.align1 = "center"
		self.valign1 = "middle"
		self.align2 = "center"
		self.valign2 = "middle"
		self.mergin = "0"
		self.fixed = "no"

		try:
			opts, args = getopt(sys.argv[1:], 'a:v:m:fs:p:d:b:h', ['align1=', 'valign1=', 'align2=', 'valign2=', 'mergin=', 'fixed', 'size=', 'pos=', 'depth=', 'bgcolor=', 'help'])
			print opts, args
		except GetoptError, e:
			print "オプションがちがいます"
			sys.exit(2)

		for o, a in opts:
			if o in ("-a", "--align1"):
				if a in ("left", "center", "right"):
					self.align1 = a
			if o in ("-v", "--valign1"):
				if a in ("top", "middle", "bottom"):
					self.valign1 = a
			if o in ("-a", "--align2"):
				if a in ("left", "center", "right"):
					self.align2 = a
			if o in ("-v", "--valign1"):
				if a in ("top", "middle", "bottom"):
					self.valign2 = a
			if o in ("-m", "--mergin"):
				self.mergin = a
			if o in ("-f", "--fixed"):
				self.fixed = "yes"
			if o in ("-h", "--help"):
				usage()
				sys.exit()

def usage():
	usage_text = """
WallPaperOptimizer: Wallpaper arranges the Optimal for MultiMoniter
Version x.x.x Copyright (C) 2011 Katsuhiro Ogikubo
See http://oggy.no-ip.info/blog/

Usage: WallpaperOptimizer [options] imgfile1 imgfile2
  [imgfile1 option]
	-a	--align1		horizontal alignment (left, center, right)
	-v	--valign1	vertical alignment (top, middle, bottom)

  [imgfile2 option]
	-a	--align2		horizontal alignment (left, center, right)
	-v	--valign2	vertical alignment (top, middle, bottom)

  [allocate option]
	-m	--mergin	left/right mergin (pixel)
	-f	--fixed		fixed imgfile allocation (nothing: change)

  [Monitor option] or ~/.wallpapositrc
	-s	--size		left/right Monitor size (pixel)
	-d	--depth		left/right Moniter color depth (8, 16, 24, 32)
	-b	--bgcolor	left/right Wallpaper base color (black)
	-h	--help
"""
	print usage_text

if __name__ == "__main__":
	wOptions = WoOption()
	print wOptions.align1
	print wOptions.valign1
	print wOptions.align2
	print wOptions.valign2
	print wOptions.mergin
	print wOptions.fixed

