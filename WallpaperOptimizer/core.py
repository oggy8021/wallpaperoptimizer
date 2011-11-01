#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ./wallpaperoptimizer  ../2560x1920.jpg ../1500x844.jpg -w

import sys
import os.path
import time
import commands
import logging
import subprocess
#from WallpaperOptimizer.debuggy import dgLine

def ConfigSettingToWorkSpace():
	logging.debug('Config Setting To WorkSpace().')

	Ws.lScreen.setSize(Config.lDisplay.getConfig()['width'], Config.lDisplay.getConfig()['height'])
	Ws.rScreen.setSize(Config.rDisplay.getConfig()['width'], Config.rDisplay.getConfig()['height'])

	if ( Ws.Size.w < (Ws.lScreen.Size.w + Ws.rScreen.Size.w) ):
		# TODO: Errorクラス
		# ほぼ設定ミスのルート
		logging.error(
		'** Workspace width[%d] < sum(left display size, right display size) [%d, %d].'
		 % ( Ws.Size.w, Ws.lScreen.Size.w, Ws.rScreen.Size.w ))
		sys.exit(2)
	if ( Ws.Size.h > Ws.lScreen.Size.h ):
		setattr(Ws.lScreen.Size, 'islessThanWorkSpaceHeight', True)
	elif ( Ws.Size.h > Ws.rScreen.Size.h ):
		setattr(Ws.rScreen.Size, 'islessThanWorkSpaceHeight', True)
	else:
		pass

	if ( Ws.lScreen.isSquare() ):
		setattr(Ws.lScreen, 'displayType', 'square')
	if ( Ws.lScreen.isWide() ):
		setattr(Ws.lScreen, 'displayType', 'wide')

	if ( Ws.rScreen.isSquare() ):
		setattr(Ws.rScreen, 'displayType', 'square')
	if ( Ws.rScreen.isWide() ):
		setattr(Ws.rScreen, 'displayType', 'wide')

	if (hasattr(Ws.lScreen.Size, 'islessThanWorkSpaceHeight')
	 and Ws.lScreen.Size.islessThanWorkSpaceHeight):
		logging.warning(
			'* Workspace height [%s] > left display height [%s].'
			 % (Ws.Size.h, Ws.lScreen.Size.h ))
	if (hasattr(Ws.rScreen.Size, 'islessThanWorkSpaceHeight')
	 and Ws.rScreen.Size.islessThanWorkSpaceHeight):
		logging.warning(
			'* Workspace height [%s] > right display height [%s].'
			 % (Ws.Size.h, Ws.rScreen.Size.h ))

	logging.debug('%20s [%s,%s]'
		 	 % ( 'display type' , Ws.lScreen.displayType, Ws.rScreen.displayType ))

	return Ws


def checkImgType(Img1, Img2):
	logging.debug('Checking imgType as Imgfile.')

	if ( Img1.getSize().w < Ws.lScreen.Size.w or Img1.getSize().w < Ws.rScreen.Size.w ):
		if ( Img1.isDual() ):
			setattr(Img1, 'imgType', 'dual')
	if ( Img2.getSize().w < Ws.lScreen.Size.w or Img2.getSize().w < Ws.rScreen.Size.w ):
		if ( Img2.isDual() ):
			setattr(Img2, 'imgType', 'dual')

	if ( Img1.isSquare() ):
		setattr(Img1, 'imgType', 'square')
	if ( Img1.isWide() ):
		setattr(Img1, 'imgType', 'wide')

	if ( Img2.isSquare() ):
		setattr(Img2, 'imgType', 'square')
	if ( Img2.isWide() ):
		setattr(Img2, 'imgType', 'wide')

	if (not hasattr(Img1, 'imgType') ):
		setattr(Img1, 'imgType', 'other')
	if (not hasattr(Img2, 'imgType') ):
		setattr(Img2, 'imgType', 'other')

	logging.debug('%20s [%s]' % ( 'imgType as Img1', Img1.imgType) )
	logging.debug('%20s [%s]' % ( 'imgType as Img2', Img2.imgType) )


def bindingImgToScreen(Img1, Img2):
	# バリエーションに対応できているか、見極められていない
	logging.debug('Binding Img to Screen.')

	if ( Option.getFixed() ):
		setattr(Img1, 'posit', 'left')
		logging.debug('%20s [%s]' % ( 'Img1 fixed binding', Img1.posit) )
		setattr(Img2, 'posit', 'right')
		logging.debug('%20s [%s]' % ( 'Img2 fixed binding', Img2.posit) )
	else:
		# アスペクト比見て、ディスプレイのタイプに応じて優先的に割り当てる
		if ( Img1.imgType == Ws.lScreen.displayType ):
			setattr(Img1, 'posit', 'left')
			logging.debug('%20s [%s]' % ( 'Img1 binding', Img1.posit) )
			setattr(Img2, 'posit', 'right')
			logging.debug('%20s [%s]' % ( 'Img2 binding', Img2.posit) )
		elif ( Img1.imgType == Ws.rScreen.displayType ):
			setattr(Img1, 'posit', 'right')
			logging.debug('%20s [%s]' % ( 'Img1 binding', Img1.posit) )
			setattr(Img2, 'posit', 'left')
			logging.debug('%20s [%s]' % ( 'Img2 binding', Img2.posit) )
		else:
			setattr(Img1, 'posit', 'left')
			logging.debug('%20s [%s]' % ( 'Img1 binding', Img1.posit) )
			setattr(Img2, 'posit', 'right')
			logging.debug('%20s [%s]' % ( 'Img2 binding', Img2.posit) )


def checkContain(Img, tmpMergin):
	logging.debug('Check Imgfile contain %s Screen.' % Img.posit)

	if ( Img.posit == 'left' ):
		# lScreenに、Imgがおさまる
		if ( Ws.lScreen.containsPlusMergin( Img, tmpMergin) ):
			return True
		else:
			return False
	else:
		# rScreenに、Imgがおさまる
		if ( Ws.rScreen.containsPlusMergin( Img, tmpMergin) ):
			return True
		else:
			return False


def downsizeImg(Img, tmpMergin):
	if ( Img.posit == 'left' ):
		tmpScreen = Ws.lScreen
	if ( Img.posit == 'right' ):
		tmpScreen = Ws.rScreen
	logging.debug('Convert Imgfile with %s Screen.' % Img.posit)

	tmpMerginW = tmpMergin[0] + tmpMergin[1]
	logging.debug('%20s [%s]' % ( 'width mergin', tmpMerginW) )
	tmpMerginH = tmpMergin[2] + tmpMergin[3]
	logging.debug('%20s [%s]' % ( 'height mergin', tmpMerginH) )

	if ( Img.getSize().w > tmpScreen.getSize().w ):
		Img.setSize( (tmpScreen.getSize().w - tmpMerginW), 
			int(max( Img.getSize().h * (tmpScreen.getSize().w - tmpMerginW) / Img.getSize().w, 1 )) )
	if ( Img.getSize().h > tmpScreen.getSize().h ):
		Img.setSize( int(max( Img.getSize().w * (tmpScreen.getSize().h - tmpMerginH) / Img.getSize().h , 1 )), 
			(tmpScreen.getSize().h - tmpMerginH) )

	Img.reSize( Img.getSize().w, Img.getSize().h)
	logging.debug('%20s [%d,%d]' % ( 'converted size', Img.getSize().w, Img.getSize().h) )


def allocateInit(Img1, Img2):
	logging.debug('Calculate center position.')

	Ws.lScreen.calcCenter()
	Ws.rScreen.calcCenter()
	Img1.calcCenter()
	Img2.calcCenter()

	logging.debug('%20s [%d,%d]' % ( 'left screen', Ws.lScreen.center.x, Ws.lScreen.center.y) )
	if (Img1.posit == 'left'):
		logging.debug('%20s [%d,%d]' % ( 'Img1', Img1.center.x, Img1.center.y) )
	else:
		logging.debug('%20s [%d,%d]' % ( 'Img2', Img2.center.x, Img2.center.y) )
	logging.debug('%20s [%d,%d]' % ( 'right screen', Ws.rScreen.center.x, Ws.rScreen.center.y) )
	if (Img1.posit == 'right'):
		logging.debug('%20s [%d,%d]' % ( 'Img1', Img1.center.x, Img1.center.y) )
	else:
		logging.debug('%20s [%d,%d]' % ( 'Img2', Img2.center.x, Img2.center.y) )


def allocateImg(Img):
	if ( Img.posit == 'left'):
		tmpScreen = Ws.lScreen
		tmpAlign = Option.getLAlign()
		tmpValign = Option.getLValign()
	else:
		tmpScreen = Ws.rScreen
		tmpAlign = Option.getRAlign()
		tmpValign = Option.getRValign()
	logging.debug('Allocate Imgfile to %s Screen.' % Img.posit)

	# 画面中央と画像中央との距離をタプルで得る
	centerDistance = (abs( Img.center.distanceX(tmpScreen.center) ) , abs( Img.center.distanceY(tmpScreen.center) ) )
	rightcornerDistance = (abs( Img.end.distanceX(tmpScreen.end) ) , abs( Img.end.distanceY(tmpScreen.end) ) )

	# Imgはインスタンス化されたときに、x,y = 0,0 つまり align=left, valign=top
	if (tmpAlign == 'center'):
		if ( Img.center.x != tmpScreen.center.x):
			Img.start.x += centerDistance[0]
			Img.end.x += centerDistance[0]
	elif (tmpAlign == 'right'):
		if ( Img.end.x != tmpScreen.end.x):
			Img.start.x += rightcornerDistance[0]
			Img.end.x += rightcornerDistance[0]

	if (tmpValign == 'middle'):
		if ( Img.center.y != tmpScreen.center.y):
			Img.start.y += centerDistance[1]
			Img.end.y += centerDistance[1]
	elif (tmpValign == 'bottom'):
		if ( Img.end.y != tmpScreen.end.y):
			Img.start.y += rightcornerDistance[1]
			Img.end.y += rightcornerDistance[1]

	logging.debug('%20s [%d,%d]' % ( 'start', Img.start.x, Img.start.y) )
	logging.debug('%20s [%d,%d]' % ( 'end', Img.end.x, Img.end.y) )


def mergeWallpaper(bkImg, Img):
	logging.debug('Merge Imgfile to %s Screen.' % Img.posit)

	if (Img.posit == 'right'):
		Img.start.x += Ws.lScreen.Size.w
		Img.end.x += Ws.lScreen.Size.w
		# center.x
	bkImg.paste( Img, (Img.start.x, Img.start.y, Img.end.x, Img.end.y) )


def optimizeWallpaper(Img1, Img2):
	logging.debug('Optimizing ... wallpapaer.')
	checkImgType(Img1, Img2)

	bindingImgToScreen(Img1, Img2)

	logging.debug('Calculate mergin.')
	lMergin = [Option.getLMergin(), 0, Option.getTopMergin(), Option.getBtmMergin()]
	logging.debug('%20s [%d,%d,%d,%d]'
			 % ( 'left display mergin', lMergin[0], lMergin[1], lMergin[2], lMergin[3] ))
	rMergin = [0, Option.getRMergin(), Option.getTopMergin(), Option.getBtmMergin()]
	logging.debug('%20s [%d,%d,%d,%d]'
			 % ( 'right display mergin', rMergin[0], rMergin[1], rMergin[2], rMergin[3] ))

	if (not checkContain(Img1, lMergin)):
		downsizeImg(Img1, lMergin)
	if (not checkContain(Img2, rMergin)):
		downsizeImg(Img2, rMergin)

	allocateInit(Img1, Img2)
	allocateImg(Img1)
	allocateImg(Img2)

	bkImg = WoImgFile('', Ws.Size.w, Ws.Size.h, Config.lDisplay.getConfig()['bgcolor'])

	mergeWallpaper(bkImg, Img1)
	mergeWallpaper(bkImg, Img2)

	return bkImg


def setWall(bkImg, tmpPath=None, flg=0):
	if (tmpPath == None):
		tmpPath = '/tmp/wallposit' + str(flg) + '.jpg'
		bkImg.save(tmpPath)
		logging.debug('Save optimized wallpaper [%s].' % tmpPath)
	else:
		# (, )だけだと、ちょっと間抜け
		tmpPath = tmpPath.replace('(','\\(')
		tmpPath = tmpPath.replace(')','\\)')

	tmpPath = os.path.abspath(tmpPath)
	ret = subprocess.call(["gconftool-2","--type","string","--set","/desktop/gnome/background/picture_filename",tmpPath])
	logging.debug('Change wallpaper to current Workspace [%s].' % tmpPath)


def daemonize():
	LChangerDir = WoChangerDir(Config.lDisplay.getConfig()['srcdir'])
	RChangerDir = WoChangerDir(Config.rDisplay.getConfig()['srcdir'])

	try:
		i = 1
		while(1):
			if (i > 2):
				i = 1
			limg = LChangerDir.getImgfileRnd()
			rimg = RChangerDir.getImgfileRnd()
			Img1 = WoImgFile(limg)
			Img2 = WoImgFile(rimg)

			bkImg = optimizeWallpaper(Img1, Img2)
			setWall(bkImg, None, i)
			interval = Option.getInterval()
			time.sleep(interval)
			i += 1
	except KeyboardInterrupt:
		sys.exit(0)


def singlerun():
	if len( Option.getArgs() ) > 1:
		Img1 = WoImgFile(Option.getLArg())
		logging.debug('Create Img1 object. [%s]' % Option.getLArg())
		logging.debug('%20s [%d,%d]' % ( 'Img1', Img1.getSize().w, Img1.getSize().h ))

		Img2 = WoImgFile(Option.getRArg())
		logging.debug('Create Img2 object. [%s]' % Option.getRArg())
		logging.debug('%20s [%s,%s]' % ( 'Img2', Img2.getSize().w, Img2.getSize().h ))

	bkImg = optimizeWallpaper(Img1, Img2)

	tmpPath = Option.getSavePath()
	if (tmpPath <> None):
		bkImg.save(tmpPath)
		logging.debug('Save optimized wallpaper [%s].' % tmpPath)

	if (Option.getSetWall()):
		setWall(bkImg)


if __name__ == "__main__":
	from WallpaperOptimizer.WoOption import WoOption
	from WallpaperOptimizer.WoConfig import WoConfig
	from WallpaperOptimizer.WoChangerDir import WoChangerDir
	from WallpaperOptimizer.Imaging.WoWorkSpace import WoWorkSpace
	from WallpaperOptimizer.Imaging.WoImgFile import WoImgFile

# 分かってないで書いている
#	dummybus = dbus.SystemBus()

# analize commandline option
	Option = WoOption()
	Verbose = Option.getVerbose()

	if (Verbose):
		loglevel = logging.DEBUG
	else:
		loglevel = logging.INFO

	logging.basicConfig(level=loglevel
						, format='%(asctime)s %(levelname)5s %(message)s'
						, filename='/tmp/wallposit.log'
						, filemode='w')
	logging.info('Starting ... wallpaperoptimizer.')

	if (Verbose):
		console = logging.StreamHandler()
		console.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
		console.setFormatter(formatter)
		logging.getLogger('').addHandler(console)


	logging.debug('Command line option as.')
	logging.debug('%20s [%s,%s].'
		 % ( 'align', Option.getLAlign(), Option.getRAlign() ))
	logging.debug('%20s [%s,%s].'
		 % ( 'valign', Option.getLValign(), Option.getRValign() ))
	logging.debug('%20s [%d,%d,%d,%d]'
		 % ( 'mergin'
		 , Option.getLMergin(), Option.getRMergin(), Option.getTopMergin(), Option.getBtmMergin() ))
	logging.debug('%20s [%s]'
		 % ( 'fixed', Option.getFixed() ))
	logging.debug('%20s [%s,%s]'
		 % ( 'display', Option.getLSize(), Option.getRSize() ))
	logging.debug('%20s [%s]'
		 % ( 'bgcolor', Option.getBgcolor() ))
	logging.debug('%20s [%s,%s]'
		 % ( 'srcdir', Option.getLSrcdir(), Option.getRSrcdir() ))
	logging.debug('%20s [%s]'
		 % ( 'setWall', Option.getSetWall() ))
	logging.debug('%20s [%s]'
		 % ( 'savepath', Option.getSavePath() ))
	logging.debug('%20s [%s]'
		 % ( 'daemon', Option.getDaemonize() ))
	logging.debug('%20s [%s]'
		 % ( 'interval', Option.getInterval() ))


# initialize workspace
	Ws = WoWorkSpace()
	logging.debug('Current WorkSpace setting as.')
	logging.debug('%20s [%d,%d]'
		 % ( 'WorkSpace Size', Ws.getSize().w, Ws.getSize().h ))
	logging.debug('%20s [%s]'
		 % ( 'WorkSpace depth', Ws.depth ))


# initialize config
	# 条件弱い？
	if (Option.getLSize() == None):
		# config set from configfile
		configfile = '~/.wallpositrc'
		configfile = os.path.expanduser(configfile)
		if (os.path.exists(configfile)):
			Config = WoConfig(configfile, None, None, Option.getBgcolor())
			logging.debug('Load configfile [%s].' % configfile)
		else:
			logging.error('** Not exists configfile [%s]. ' % configfile)
			sys.exit(2)
		logging.debug('Config set from configfile.')
	else:
		# config set from commandline option
		Config = WoConfig(None, Option.getLSize(), Option.getRSize(), Option.getBgcolor(), [Option.getLSrcdir(), Option.getRSrcdir()])
		logging.debug('Config set from commandline option.')

	logging.debug('%20s [%s,%s]'
			 % ( 'left display size'
			 , Config.lDisplay.getConfig()['width'], Config.rDisplay.getConfig()['width'] ))
	logging.debug('%20s [%s,%s]'
			 % ( 'right display size'
			 , Config.lDisplay.getConfig()['height'], Config.rDisplay.getConfig()['height'] ))
	logging.debug('%20s [%s,%s]'
			 % ( 'position'
			 , Config.lDisplay.getConfig()['posit'], Config.rDisplay.getConfig()['posit'] ))
	logging.debug('%20s [%s,%s]'
			 % ( 'bgcolor'
			 , Config.lDisplay.getConfig()['bgcolor'], Config.rDisplay.getConfig()['bgcolor'] ))
	logging.debug('%20s [%s]'
			 % ( 'srcdir to left'
			 , Config.lDisplay.getConfig()['srcdir'] ))
	logging.debug('%20s [%s]'
			 % ( 'srcdir to right'
			 , Config.rDisplay.getConfig()['srcdir'] ))

	Ws = ConfigSettingToWorkSpace()

	if (Option.getDaemonize()):
		logging.debug('Running ... daemonize mode.')
		daemonize()
	else:
		logging.debug('Running ... singlerun mode.')
		singlerun()

	logging.debug('Quit ... wallpaperoptimizer.')
	sys.exit(0)
