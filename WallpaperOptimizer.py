# -*- coding: utf-8 -*-

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
		setattr(ws.lScreen.Size.h, 'islessThanWorkSpace', True)
	elif ( ws.Size.h > ws.rScreen.Size.h ):
		setattr(ws.rScreen.Size.h, 'islessThanWorkSpace', True)
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

	return ws

if __name__ == "__main__":
	ws = ConfigSetting()
	print ws.lScreen.displayType
	print ws.rScreen.displayType
	if (getattr(ws.lScreen.Size.h, islessThanWorkSpace) and ws.lScreen.Size.h.islessThanWorkSpace):
		print 'Warning: 左ディスプレイの高さがワークスペースに対して低いです。', ws.lScreen.Size.h
	if (getattr(ws.rScreen.Size.h, islessThanWorkSpace) and ws.rScreen.Size.h.islessThanWorkSpace):
		print 'Warning: 右ディスプレイの高さがワークスペースに対して低いです。', ws.rScreen.Size.h
