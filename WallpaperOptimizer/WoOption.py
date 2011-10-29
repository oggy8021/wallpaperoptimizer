# -*- coding: utf-8 -*-

from optparse import Option, OptionParser, OptionValueError

class WoOption(object):

	def __init__(self):
		class MultiargOption(Option):
			ACTIONS = Option.ACTIONS + ("multistore", "quatrostore", "doublestore", )
			STORE_ACTIONS = Option.STORE_ACTIONS + ("multistore", "quatrostore", "doublestore", )
			TYPED_ACTIONS = Option.TYPED_ACTIONS + ("multistore", "quatrostore", "doublestore", )
			ALWAYS_TYPED_ACTIONS = Option.ALWAYS_TYPED_ACTIONS + ("multistore", "quatrostore", "doublestore", )

			def take_action(self, action, dest, opt, value, values, parser):
				def exchangeValue(lvalue, dest, values):
					for idx,m in enumerate(lvalue):
						if (m <> ""):
							vals = getattr(values, dest)
							vals[idx] = lvalue[idx]
							setattr(values, dest, vals)

				if action == "multistore":
					lvalue = value.split(",")
					if (len(lvalue) > 1 and len(lvalue) <= 2):
						exchangeValue(lvalue, dest, values)
					else:
						raise OptionValueError("option: %s to 2 values." % dest)
				elif action == "quatrostore":
					lvalue = value.split(",")
					if (len(lvalue) > 1 and len(lvalue) <= 4):
						exchangeValue(lvalue, dest, values)
					else:
						raise OptionValueError("option: %s to 2 values." % dest)
				elif action == "doublestore":
					lvalue = value.split(",")
					if (len(lvalue) > 1 and len(lvalue) <= 2 and lvalue[0] <> "" and lvalue[1] <> ""):
						exchangeValue(lvalue, dest, values)
					else:
						raise OptionValueError("option: %s necessary 2 values." % dest)
				else:
					Option.take_action(self, action, dest, opt, value, values, parser)

		parser = OptionParser(usage="%prog [options] imgfile1 imgfile2"
					, version="%prog 0.2.0"
					, option_class=MultiargOption)
		parser.set_defaults(align=["center","center"]
					, valign=["middle","middle"]
					, mergin=[0,0,0,0]
					, fixed=False
					, size=[None, None]
					, bgcolor="black"
					, srcdir=['.','.']
					, save=None
					, wall=False
					, verbose=False
					, daemonize=False
					, interval=60)

		parser.add_option("-a", "--align", dest="align", action="multistore"
					, metavar="left,center,right"
					, help="horizontal alignment (left, center, right)")
		parser.add_option("-v", "--valign", dest="valign", action="multistore"
					, metavar="top,middle,bottom"
					, help="vertical alignment (top, middle, bottom)")
		parser.add_option("-m", "--mergin", dest="mergin", action="quatrostore"
					, metavar="pixel,pixel,pixel,pixel"
					, help="left/right/top/bottom mergin for WorkSpace")
		parser.add_option("-f", "--fixed", dest="fixed", action="store_true"
					, help="fixed imgfile allocation (nothing: Optimize)")
		parser.add_option("-d", "--display", dest="size", action="doublestore"
					, metavar="pixel x pixel"
					, help="left/right Display size")
		parser.add_option("-b", "--bgcolor", dest="bgcolor", action="store", type="string"
					, metavar="color, 0xRRGGBB"
					, help="left/right Wallpaper base color (default: black)")
		parser.add_option("-S", "--srcdir", dest="srcdir", action="doublestore", type="string"
					, metavar="PATH,PATH"
					, help="wallpaper src dir")
		parser.add_option("-s", "--save", dest="save", action="store"
					, metavar="PATH"
					, help="Save Wallpaper to PATH")
		parser.add_option("-w", "--wall", dest="wall", action="store_true"
					, help="Created wallpaper set to current WorkSpace")
		parser.add_option("-V", "--verbose", dest="verbose", action="store_true"
					, help="verbose")
		parser.add_option("-D", "--daemon", dest="daemonize", action="store_true"
					, help="daemonize (default: False)")
		parser.add_option("-i", "--interval", dest="interval", action="store", type="int"
					, metavar="sec"
					, help="change wallpaper interval (default: 60sec)")

		(self.opts, self.args) = parser.parse_args()
		if (len(self.args) < 1 and self.opts.daemonize == False):
			parser.error("Please set imgfile parameter.")

		for m_align in self.opts.align:
			if m_align in ("left", "center", "right"):
				break
			raise OptionValueError("option: align invalid")

		for m_valign in self.opts.valign:
			if m_valign in ("top", "middle", "bottom"):
				break
			raise OptionValueError("option: valign invalid")

		import re
		ptn = re.compile('^0x(.+)$')
		if (ptn.match(self.opts.bgcolor)):
			subStr = ptn.split(self.opts.bgcolor)
			self.opts.bgcolor = '#%s' % subStr[1]

	def getLAlign(self):
		return self.opts.align[0]

	def getRAlign(self):
		return self.opts.align[1]

	def getLValign(self):
		return self.opts.valign[0]

	def getRValign(self):
		return self.opts.valign[1]

	def getLMergin(self):
		return int(self.opts.mergin[0])

	def getRMergin(self):
		return int(self.opts.mergin[1])

	def getTopMergin(self):
		return int(self.opts.mergin[2])

	def getBtmMergin(self):
		return int(self.opts.mergin[3])

	def getFixed(self):
		return self.opts.fixed

	def getLSize(self):
		return self.opts.size[0]

	def getRSize(self):
		return self.opts.size[1]

	def getBgcolor(self):
		return self.opts.bgcolor

	def getLSrcdir(self):
		return self.opts.srcdir[0]

	def getRSrcdir(self):
		return self.opts.srcdir[1]

	def getVerbose(self):
		return self.opts.verbose

	def getSavePath(self):
		return self.opts.save

	def getSetWall(self):
		return self.opts.wall

	def getDaemonize(self):
		return self.opts.daemonize

	def getInterval(self):
		return self.opts.interval

	def getLArg(self):
		return self.args[0]

	def getRArg(self):
		return self.args[1]

	def getArgs(self):
		return self.args

if __name__ == "__main__":
	wOption = WoOption()
#	print wOption.getLAlign()
#	print wOption.getRAlign()
#	print wOption.getLSize()
#	print wOption.getRSize()
#	print wOption.getBgcolor()
	print wOption.getLSrcdir()
	print wOption.getRSrcdir()
#	print wOption.getVerbose()
