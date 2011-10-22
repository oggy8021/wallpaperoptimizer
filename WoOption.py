# -*- coding: utf-8 -*-

from optparse import Option, OptionParser, OptionValueError

class WoOption(object):

	def __init__(self):
		class MultiargOption(Option):
			ACTIONS = Option.ACTIONS + ("multistore", "doublestore", )
			STORE_ACTIONS = Option.STORE_ACTIONS + ("multistore", "doublestore", )
			TYPED_ACTIONS = Option.TYPED_ACTIONS + ("multistore", "doublestore", )
			ALWAYS_TYPED_ACTIONS = Option.ALWAYS_TYPED_ACTIONS + ("multistore", "doublestore", )
			
			def take_action(self, action, dest, opt, value, values, parser):
				if action == "multistore":
					lvalue = value.split(",")
					if (len(lvalue) > 1 and len(lvalue) <= 2):
						for idx,m in enumerate(lvalue):
							if (m <> ""):
								vals = getattr(values, dest)
								vals[idx] = lvalue[idx]
								setattr(values, dest, vals)
					else:
						raise OptionValueError("option: %s to 2 values." % dest)
				elif action == "doublestore":
					lvalue = value.split(",")
					if (len(lvalue) > 1 and len(lvalue) <= 2 and lvalue[0] <> "" and lvalue[1] <> ""):
						for idx,m in enumerate(lvalue):
							if (m <> ""):
								vals = getattr(values, dest)
								vals[idx] = lvalue[idx]
								setattr(values, dest, vals)
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
					, fixed=True
					, size=[None, None]
					, bgcolor="black"
					, verbose=False)

		parser.add_option("-a", "--align", dest="align", action="multistore"
					, metavar="left,center,right"
					, help="horizontal alignment (left, center, right)")
		parser.add_option("-v", "--valign", dest="valign", action="multistore"
					, metavar="top,middle,bottom"
					, help="vertical alignment (top, middle, bottom)")
		parser.add_option("-m", "--mergin", dest="mergin", action="multistore"
					, metavar="pixel"
					, help="left/right mergin (pixel, pixel)")
		parser.add_option("-f", "--fixed", dest="fixed", action="store_true"
					, help="fixed imgfile allocation (nothing: change)")
		parser.add_option("-s", "--size", dest="size", action="doublestore"
					, metavar="pixel"
					, help="left/right Monitor size (pixel x pixel)")
		parser.add_option("-b", "--bgcolor", dest="bgcolor", action="store"
					, metavar="color, #hex color"
					, help="left/right Wallpaper base color (black)")
		parser.add_option("-V", "--verbose", action="store_true"
					, help="verbose")

		(self.opts, self.args) = parser.parse_args()
		if (len(self.args) < 1):
			parser.error("Please set imgfile parameter.")

		for m_align in self.opts.align:
			if m_align in ("left", "center", "right"):
				break
			raise OptionValueError("option: align invalid")

		for m_valign in self.opts.valign:
			if m_valign in ("top", "middle", "bottom"):
				break
			raise OptionValueError("option: valign invalid")

	def getArgs(self):
		return self.args

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

	def getVerbose(self):
		return self.opts.verbose

	def getLArg(self):
		return self.args[0]

	def getRArg(self):
		return self.args[1]

	def getSaveArg(self):
		return self.args[2]

if __name__ == "__main__":
	wOption = WoOption()
	print wOption.getLAlign()
	print wOption.getRAlign()
	print wOption.getLSize()
	print wOption.getRSize()
	print wOption.getVerbose()
