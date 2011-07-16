#!/usr/bin/env python

#coding: UTF-8

import datetime
#import locale

def debugCon (val):
	td = datetime.datetime.now()
	print td.strftime("%Y/%m/%d %H:%M:%S") + ' [debug] :' + str(val) + '.\n'

#debugCon("hoge")
