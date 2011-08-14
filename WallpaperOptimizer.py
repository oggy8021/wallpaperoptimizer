# -*- coding: utf-8 -*-

from debuggy import dgLine
from var_dump import var_dump

def ConfigSetting():
	ws.lScreen.setSize(wConfig.lDisplay.getConfig()['width'], wConfig.lDisplay.getConfig()['height'])
	ws.rScreen.setSize(wConfig.rDisplay.getConfig()['width'], wConfig.rDisplay.getConfig()['height'])

	if ( ws.Size.w < (ws.lScreen.Size.w + ws.rScreen.Size.w) ):
		# TODO: Errorクラス
		# ほぼ設定ミス
		print 'Error: ワークスペースの幅が左右ディスプレイの幅の合計より小さいです。', ws.Size.w, ws.lScreen.Size.w, ws.rScreen.Size.w
		return False
	if ( ws.Size.h > ws.lScreen.Size.h ):
		setattr(ws.lScreen.Size, 'islessThanWorkSpaceHeight', True)
	elif ( ws.Size.h > ws.rScreen.Size.h ):
		setattr(ws.rScreen.Size, 'islessThanWorkSpaceHeight', True)
	else:
		pass

	if ( ws.lScreen.isSquare() ):
		setattr(ws.lScreen, 'displayType', 'square')
	if ( ws.lScreen.isWide() ):
		setattr(ws.lScreen, 'displayType', 'wide')

	if ( ws.rScreen.isSquare() ):
		setattr(ws.rScreen, 'displayType', 'square')
	if ( ws.rScreen.isWide() ):
		setattr(ws.rScreen, 'displayType', 'wide')

	if (hasattr(ws.lScreen.Size, 'islessThanWorkSpaceHeight') and ws.lScreen.Size.islessThanWorkSpaceHeight):
		print 'Warning: 左ディスプレイの高さがワークスペースに対して低いです。', ws.lScreen.Size.h
	if (hasattr(ws.rScreen.Size, 'islessThanWorkSpaceHeight') and ws.rScreen.Size.islessThanWorkSpaceHeight):
		print 'Warning: 右ディスプレイの高さがワークスペースに対して低いです。', ws.rScreen.Size.h

	dgLine( ws.lScreen.displayType , 'ws.lScreen.displayType')
	dgLine( ws.rScreen.displayType , 'ws.rScreen.displayType')

	return ws


def checkImgType():
	if ( Img1.getSize().w < ws.lScreen.Size.w or Img1.getSize().w < ws.rScreen.Size.w ):
		if ( Img1.isDual() ):
			setattr(Img1, 'imgType', 'dual')
	if ( Img2.getSize().w < ws.lScreen.Size.w or Img2.getSize().w < ws.rScreen.Size.w ):
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

	dgLine( Img1.imgType , 'Img1.imgType' )
	dgLine( Img2.imgType , 'Img2.imgType' )


def bindingImgToScreen():
	# バリエーションに対応できているか、見極められていない
	if ( Img1.imgType == ws.lScreen.displayType ):
		setattr(Img1, 'posit', 'left')
		if ( Img2.imgType == ws.rScreen.displayType ):
			setattr(Img2, 'posit', 'right')

	if ( Img2.imgType == ws.lScreen.displayType ):
		setattr(Img2, 'posit', 'left')
		if ( Img1.imgType == ws.rScreen.displayType ):
			setattr(Img1, 'posit', 'right')

	if ( not getattr(Img1, 'posit', False) ):
		setattr(Img1, 'posit', 'left')
	if ( not getattr(Img2, 'posit', False) ):
		setattr(Img2, 'posit', 'right')

	dgLine ( Img1.posit , 'Img1.posit')
	dgLine ( Img2.posit , 'Img2.posit')


def checkContain(Img):
	if ( Img.posit == 'left' ):
		if ( ws.lScreen.contains( Img ) ):
			return True
		else:
			return False
	else:
		if ( ws.rScreen.contains( Img ) ):
			return True
		else:
			return False


def downsizeImg(Img):
	if ( Img.posit == 'left' ):
		tmpScreen = ws.lScreen
	if ( Img.posit == 'right' ):
		tmpScreen = ws.rScreen

	if ( Img.getSize().w > tmpScreen.getSize().w ):
		Img.setSize( tmpScreen.getSize().w, int(max( Img.getSize().h * tmpScreen.getSize().w / Img.getSize().w, 1 )) )
	if ( Img.getSize().h > tmpScreen.getSize().h ):
		Img.setSize( int(max( Img.getSize().w * tmpScreen.getSize().h / Img.getSize().h , 1 )), tmpScreen.getSize().h )

	Img.reSize( Img.getSize().w, Img.getSize().h )
	dgLine(Img.getSize().w , 'Img.getSize().w downSize later')
	dgLine(Img.getSize().h , 'Img.getSize().h downSize later')
	dgLine(Img.isSquare() , 'Img.isSquare()')


def allocateInit():
	ws.lScreen.calcCenter()
	ws.rScreen.calcCenter()
	Img1.calcCenter()
	Img2.calcCenter()

	dgLine(ws.lScreen.center.x, 'ws.lScreen.center.x')
	dgLine(ws.lScreen.center.y, 'ws.lScreen.center.y')
	dgLine(ws.rScreen.center.x, 'ws.rScreen.center.x')
	dgLine(ws.rScreen.center.y, 'ws.rScreen.center.y')
	dgLine(Img1.center.x, 'Img1.center.x')
	dgLine(Img1.center.y, 'Img1.center.y')
	dgLine(Img2.center.x, 'Img2.center.x')
	dgLine(Img2.center.y, 'Img2.center.y')


def allocateImg(Img):
	if ( Img.posit == 'left'):
		tmpScreen = ws.lScreen
	else:
		tmpScreen = ws.rScreen

	tmpDistance = (abs( Img.center.distanceX(tmpScreen.center) ) , abs( Img.center.distanceY(tmpScreen.center) ) )
	if ( Img.center.x != tmpScreen.center.x):
		Img.start.x += tmpDistance[0]
		Img.end.x += tmpDistance[1]
	if ( Img.center.y != tmpScreen.center.y):
		Img.start.y += tmpDistance[0]
		Img.end.x += tmpDistance[1]
	dgLine(Img.center.x, 'Img.center.x')
	dgLine(Img.center.y, 'Img.center.y')

	dgLine(Img.start.x, 'Img.start.x')
	dgLine(Img.start.y, 'Img.start.y')


def mergeWallpaper(bkImg, Img):
	pass


if __name__ == "__main__":
	from WoConfig import WoConfig
	from WoWorkSpace import WoWorkSpace
	import sys
	from WoImgFile import WoImgFile

	wConfig = WoConfig()
	ws = WoWorkSpace()

	ws = ConfigSetting()

	if len(sys.argv) > 1:
		Img1 = WoImgFile(sys.argv[1])
		Img2 = WoImgFile(sys.argv[2])
		dgLine( Img1.getSize().w , 'Img1 width')
		dgLine( Img1.getSize().h , 'Img1 height')
		dgLine( Img2.getSize().w , 'Img2 width')
		dgLine( Img2.getSize().h , 'Img2 height')

	checkImgType()

	bindingImgToScreen()

	if (not checkContain(Img1) ):
		downsizeImg(Img1)
	if (not checkContain(Img2) ):
		downsizeImg(Img2)

	allocateInit()
	allocateImg(Img1)
	allocateImg(Img2)

	bkImg = WoImgFile('', ws.Size.w, ws.Size.h, wConfig.lDisplay.getConfig()['bgcolor'])
	mergeWallpaper(bkImg, Img1)
	mergeWallpaper(bkImg, Img2)
