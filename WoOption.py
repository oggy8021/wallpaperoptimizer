# -*- coding: utf-8 -*-

from optparse import Option, OptionParser

class WoOption(object):

	class MultiavgOption(Option):
		ACTIONS = Option.ACTIONS + ("multiavg", )
		STORE_ACTIONS = Option.STORE_ACTIONS + ("multiavg", )
		TYPED_ACTIONS = Option.TYPED_ACTIONS + ("multiavg", )
		ALWAYS_TYPED_ACTIONS = Option.ALWAYS_TYPED_ACTIONS + ("multiavg", )
		
		def take_action(self, action, dest, opt, value, values, parser):
			if action == "multiavg":
				lvalue = value.split(",")
				setattr(values, dest, lvalue)
#				values.ensure_value(dest, []).extend(lvalue)
			else:
				Option.take_action(self, action, dest, opt, value, values, parser)

	parser = OptionParser(usage="%prog [options] imgfile1 imgfile2"
				, version="%prog 0.2.0"
				, option_class=MultiavgOption)
	parser.set_defaults(align=["center","center"], valign=["middle","middle"], mergin=0, fixed=True)
	parser.add_option("-a", "--align", dest="align", action="multiavg"
#				, choices=('left', 'center', 'right')
				, help="horizontal alignment (left, center, right)")
	parser.add_option("-v", "--valign", dest="valign", action="multiavg"
#				, choices=('top', 'middle', 'bottom')
				, help="vertical alignment (top, middle, bottom)")
	parser.add_option("-m", "--mergin", dest="mergin"
				, help="left/right mergin (pixel)", type="int")
	parser.add_option("-f", "--fixed", dest="fixed", action="store_true"
				, help="fixed imgfile allocation (nothing: change)")
	parser.add_option("-s", "--size", dest="size"
				, help="left/right Monitor size (pixel)")
	parser.add_option("-d", "--depth", dest="depth"
				, choices=('8', '16', '24', '32')
				, help="left/right Moniter color depth (8, 16, 24, 32)")
#TODO: moji->int
	parser.add_option("-b", "--bgcolor", dest="bgcolor"
				, help="left/right Wallpaper base color (black)")

	(opts, args) = parser.parse_args()
#	if (len(args) < 1):
#		parser.error("Please set imgfile parameter.")
	print '\n' , opts, args

if __name__ == "__main__":
	wOptions = WoOption()

#	print wOptions.opts.align
