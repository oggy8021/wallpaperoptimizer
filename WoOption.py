# -*- coding: utf-8 -*-

from optparse import Option, OptionParser, OptionValueError
from debuggy import dgLine

class WoOption(object):

	def __init__(self):
		class MultiargOption(Option):
			ACTIONS = Option.ACTIONS + ("multiavg", )
			STORE_ACTIONS = Option.STORE_ACTIONS + ("multiavg", )
			TYPED_ACTIONS = Option.TYPED_ACTIONS + ("multiavg", )
			ALWAYS_TYPED_ACTIONS = Option.ALWAYS_TYPED_ACTIONS + ("multiavg", )
			
			def take_action(self, action, dest, opt, value, values, parser):
				if action == "multiavg":
					lvalue = value.split(",")
					for m in lvalue:
						if (m <> ""):
							idx = lvalue.index(m)
							vals = getattr(values, dest)
							vals[idx] = lvalue[idx]
							setattr(values, dest, vals)
				else:
					Option.take_action(self, action, dest, opt, value, values, parser)

		parser = OptionParser(usage="%prog [options] imgfile1 imgfile2"
					, version="%prog 0.2.0"
					, option_class=MultiargOption)
		parser.set_defaults(align=["center","center"]
					, valign=["middle","middle"]
					, mergin=0
					, fixed=True
					, size=["1024x768","1024x768"]
					, bgcolor="black")

		parser.add_option("-a", "--align", dest="align", action="multiavg"
					, metavar="left,center,right"
					, help="horizontal alignment (left, center, right)")
		parser.add_option("-v", "--valign", dest="valign", action="multiavg"
					, metavar="top,middle,bottom"
					, help="vertical alignment (top, middle, bottom)")
		parser.add_option("-m", "--mergin", dest="mergin", metavar="pixel"
					, help="left/right mergin (pixel)", type="int")
		parser.add_option("-f", "--fixed", dest="fixed", action="store_true"
					, help="fixed imgfile allocation (nothing: change)")

		parser.add_option("-s", "--size", dest="size", action="multiavg"
					, metavar="pixel"
					, help="left/right Monitor size (pixel x pixel)")
		parser.add_option("-b", "--bgcolor", dest="bgcolor", action="store"
					, metavar="color, #hex color"
					, help="left/right Wallpaper base color (black)")

		(self.opts, self.args) = parser.parse_args()
#	if (len(args) < 1):
#		parser.error("Please set imgfile parameter.")

		if ("" in self.opts.align):
			idx = self.opts.align.index("")
			self.opts.align.remove("")
			self.opts.align.insert(idx, "center")
		for m_align in self.opts.align:
			if m_align in ("left", "center", "right"):
				break
			raise OptionValueError("option: align invalid")

		if ("" in self.opts.valign):
			idx = self.opts.valign.index("")
			self.opts.valign.remove("")
			self.opts.valign.insert(idx, "middle")
		for m_valign in self.opts.valign:
			if m_valign in ("top", "middle", "bottom"):
				break
			raise OptionValueError("option: valign invalid")

	def getOption(self):
		option = dict()
		option['align'] = self.opts.align
		option['valign'] = self.opts.valign
		option['mergin'] = self.opts.mergin
		option['fixed'] = self.opts.fixed
		option['size'] = self.opts.size
		option['bgcolor'] = self.opts.bgcolor
		return option

	def getArgs(self):
		return self.args

if __name__ == "__main__":
	wOptions = WoOption()
	dgLine( wOptions.getOption()['align'] )
	dgLine( wOptions.getOption()['valign'] )
	dgLine( wOptions.getOption()['mergin'] )
	dgLine( wOptions.getOption()['fixed'] )
	dgLine( wOptions.getOption()['size'] )
	dgLine( wOptions.getOption()['bgcolor'] )
	dgLine( wOptions.getArgs() )
