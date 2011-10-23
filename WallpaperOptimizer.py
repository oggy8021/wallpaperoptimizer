# -*- coding: utf-8 -*-

#python WallpaperOptimizer.py ../2560x1920.jpg ../1500x844.jpg ../WallPosit_test.jpg

from debuggy import dgLine
from var_dump import var_dump
import sys
import os.path

def ConfigSettingToWorkSpace():
	Ws.lScreen.setSize(Config.lDisplay.getConfig()['width'], Config.lDisplay.getConfig()['height'])
	Ws.rScreen.setSize(Config.rDisplay.getConfig()['width'], Config.rDisplay.getConfig()['height'])

	if ( Ws.Size.w < (Ws.lScreen.Size.w + Ws.rScreen.Size.w) ):
		# TODO: Errorクラス
		# ほぼ設定ミスのルート
		print 'Error: ワークスペースの幅が左右ディスプレイの幅の合計より小さいです。', Ws.Size.w, Ws.lScreen.Size.w, Ws.rScreen.Size.w
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

	if (hasattr(Ws.lScreen.Size, 'islessThanWorkSpaceHeight') and Ws.lScreen.Size.islessThanWorkSpaceHeight):
		print 'Warning: 左ディスプレイの高さがワークスペースに対して低いです。', Ws.lScreen.Size.h
	if (hasattr(Ws.rScreen.Size, 'islessThanWorkSpaceHeight') and Ws.rScreen.Size.islessThanWorkSpaceHeight):
		print 'Warning: 右ディスプレイの高さがワークスペースに対して低いです。', Ws.rScreen.Size.h

	if (Verbose):
		dgLine( Ws.lScreen.displayType , 'Ws.lScreen.displayType')
		dgLine( Ws.rScreen.displayType , 'Ws.rScreen.displayType')

	return Ws


def checkImgType():
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

	if (Verbose):
		dgLine( Img1.imgType , 'Img1.imgType' )
		dgLine( Img2.imgType , 'Img2.imgType' )


def bindingImgToScreen():
	# バリエーションに対応できているか、見極められていない

	if ( Option.getFixed() ):
		setattr(Img1, 'posit', 'left')
		setattr(Img2, 'posit', 'right')
	else:
		# アスペクト比見て、ディスプレイのタイプに応じて優先的に割り当てる
		if ( Img1.imgType == Ws.lScreen.displayType ):
			setattr(Img1, 'posit', 'left')
#			print 1
			if ( Img2.imgType == Ws.rScreen.displayType ):
				setattr(Img2, 'posit', 'right')
#				print 2
		elif ( Img2.imgType == Ws.lScreen.displayType ):
			setattr(Img2, 'posit', 'left')
#			print 3
			if ( Img1.imgType == Ws.rScreen.displayType ):
				setattr(Img1, 'posit', 'right')
#				print 4

		# 割り当てを上書きしている可能性があるので、補間する
		if ( not getattr(Img1, 'posit', False) ):
			setattr(Img1, 'posit', 'left')
#			print 5
		if ( not getattr(Img2, 'posit', False) ):
			setattr(Img2, 'posit', 'right')
#			print 6

	if (Verbose):
		dgLine ( Img1.posit , 'Img1.posit')
		dgLine ( Img2.posit , 'Img2.posit')


def checkContain(Img, tmpMergin):
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
	tmpMerginW = tmpMergin[0] + tmpMergin[1]
	tmpMerginH = tmpMergin[2] + tmpMergin[3]

	if ( Img.getSize().w > tmpScreen.getSize().w ):
		Img.setSize( (tmpScreen.getSize().w - tmpMerginW), 
			int(max( Img.getSize().h * (tmpScreen.getSize().w - tmpMerginW) / Img.getSize().w, 1 )) )
	if ( Img.getSize().h > tmpScreen.getSize().h ):
		Img.setSize( int(max( Img.getSize().w * (tmpScreen.getSize().h - tmpMerginH) / Img.getSize().h , 1 )), 
			(tmpScreen.getSize().h - tmpMerginH) )

	Img.reSize( Img.getSize().w, Img.getSize().h)

	if (Verbose):
		dgLine(Img.getSize().w , 'Img.getSize(%s).w downSize later' % Img.posit)
		dgLine(Img.getSize().h , 'Img.getSize(%s).h downSize later' % Img.posit)
		dgLine(Img.isSquare() , 'Img.isSquare()')


def allocateInit():
	Ws.lScreen.calcCenter()
	Ws.rScreen.calcCenter()
	Img1.calcCenter()
	Img2.calcCenter()

	if (Verbose):
		dgLine(Ws.lScreen.center.x, 'Ws.lScreen.center.x')
		dgLine(Ws.lScreen.center.y, 'Ws.lScreen.center.y')
		dgLine(Img1.center.x, 'Img1.center.x')
		dgLine(Img1.center.y, 'Img1.center.y')
		dgLine(Ws.rScreen.center.x, 'Ws.rScreen.center.x')
		dgLine(Ws.rScreen.center.y, 'Ws.rScreen.center.y')
		dgLine(Img2.center.x, 'Img2.center.x')
		dgLine(Img2.center.y, 'Img2.center.y')


def allocateImg(Img):
	if ( Img.posit == 'left'):
		tmpScreen = Ws.lScreen
		tmpAlign = Option.getLAlign()
		tmpValign = Option.getLValign()
	else:
		tmpScreen = Ws.rScreen
		tmpAlign = Option.getRAlign()
		tmpValign = Option.getRValign()

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

	if (Verbose):
#		dgLine(tmpAlign, 'tmpAlign')
#		dgLine(tmpValign, 'tmpValign')
		dgLine(Img.start.x, 'Img.start.x')
		dgLine(Img.start.y, 'Img.start.y')
		dgLine(Img.end.x, 'Img.end.x')
		dgLine(Img.end.y, 'Img.end.y')


def mergeWallpaper(bkImg, Img):
	if (Img.posit == 'right'):
		Img.start.x += Ws.lScreen.Size.w
		Img.end.x += Ws.lScreen.Size.w
		# center.x
	bkImg.paste( Img, (Img.start.x, Img.start.y, Img.end.x, Img.end.y) )


if __name__ == "__main__":
	from WoOption import WoOption
	from WoConfig import WoConfig
	from WoWorkSpace import WoWorkSpace
	from WoImgFile import WoImgFile

	#new
	Option = WoOption()
	Verbose = Option.getVerbose()
	Ws = WoWorkSpace()

	if (Option.getLSize() == None):
		# ディスプレイサイズがオプションにて、指定されていない
		configfile = '~/.wallpositrc'
		configfile = os.path.expanduser(configfile)
		if (os.path.exists(configfile)):
			Config = WoConfig(configfile, None, None, Option.getBgcolor())
		else:
			print 'Error: 設定ファイル %s がありません。' % configfile
			sys.exit(2)
	else:
		# ディスプレイサイズがオプションにて、指定されている
		Config = WoConfig(None, Option.getLSize(), Option.getRSize(), Option.getBgcolor())

	#function
	Ws = ConfigSettingToWorkSpace()

	if len( Option.getArgs() ) > 1:
		Img1 = WoImgFile(Option.getLArg())
		Img2 = WoImgFile(Option.getRArg())
		if (Verbose):
			dgLine( Img1.getSize().w , 'Img1 width')
			dgLine( Img1.getSize().h , 'Img1 height')
			dgLine( Img2.getSize().w , 'Img2 width')
			dgLine( Img2.getSize().h , 'Img2 height')

	#function
	checkImgType()

	#function
	bindingImgToScreen()

	lMergin = [Option.getLMergin(), 0, Option.getTopMergin(), Option.getBtmMergin()]
	rMergin = [0, Option.getRMergin(), Option.getTopMergin(), Option.getBtmMergin()]

	if (not checkContain(Img1, lMergin)):
		#function
		downsizeImg(Img1, lMergin)
	if (not checkContain(Img2, rMergin)):
		#function
		downsizeImg(Img2, rMergin)

	#function
	allocateInit()
	allocateImg(Img1)
	allocateImg(Img2)

	#new
	bkImg = WoImgFile('', Ws.Size.w, Ws.Size.h, Config.lDisplay.getConfig()['bgcolor'])
	#function
	mergeWallpaper(bkImg, Img1)
	mergeWallpaper(bkImg, Img2)

	bkImg.save(Option.getSaveArg())
