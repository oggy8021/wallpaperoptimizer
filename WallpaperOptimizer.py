# -*- coding: utf-8 -*-

from debuggy import dgLog

def ConfigSetting():
	from WoConfig import WoConfig
	wConfig = WoConfig()

	from WoWorkSpace import WoWorkSpace
	ws = WoWorkSpace()

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

	dgLog( ws.lScreen.displayType )
	dgLog( ws.rScreen.displayType )

	return ws

def loadImage(Img1=None, Img2=None):
	import sys
	from WoImgFile import WoImgFile
	if len(sys.argv) > 1:
		Img1 = WoImgFile(sys.argv[1])
		Img2 = WoImgFile(sys.argv[2])

	dgLog( Img1.getSize().w )
	dgLog( Img1.getSize().h )
	dgLog( Img2.getSize().w )
	dgLog( Img2.getSize().h )

def checkContain(ws, Img1, Img2):
	pass
#	if ( ws.lScreen.contains(Img1) )

if __name__ == "__main__":
	ws = ConfigSetting()
	Img1 = None
	Img2 = None
	loadImage(Img1, Img2)
