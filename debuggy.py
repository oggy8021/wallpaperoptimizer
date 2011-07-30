#!/usr/bin/env python

# -*- coding: utf-8 -*-

import datetime
import re
#import locale

def dgConv(val):
	ptn = re.compile(r'^<type\s\'(.+)\'>$')
	subStr = ptn.search( str( type(val) ) )
	tp = subStr.group(1) 
	if tp == 'int' or tp == 'float' or tp == 'double':
		return str(val)
	elif tp == 'Instance':
		pass
	else:
		return str(val)

def dgLine(val):
	print dgConv(val)

def dgLog(val):
	td = datetime.datetime.now()
	print td.strftime("%Y/%m/%d %H:%M:%S") + ' [debug] :' + dgConv(val) + '.\n',


if __name__ == "__main__":
	dgLine('fuga')
	dgLine(1)
	dgLine(0.001)
	n = 300
	dgLine(n)
	l = 300
	dgLine(l)
	dgLog(0.002)
