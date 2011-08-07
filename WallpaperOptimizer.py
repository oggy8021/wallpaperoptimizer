# -*- coding: utf-8 -*-

def ConfigSetting():
	from WoConfig import WoConfig
	wConfig = WoConfig()

	from WoWorkSpace import WoWorkSpace
	ws = WoWorkSpace()

	print wConfig.lScreen.getConfig()['width'], wConfig.lScreen.getConfig()['height']
	print wConfig.rScreen.getConfig()['width'], wConfig.rScreen.getConfig()['height']
	ws.lScreen.setSize(wConfig.lScreen.getConfig()['width'], wConfig.lScreen.getConfig()['height'])
	ws.rScreen.setSize(wConfig.rScreen.getConfig()['width'], wConfig.rScreen.getConfig()['height'])

	print ws.lScreen.getSize()
	print ws.rScreen.getSize()

	if ( ws.Size[0] < (ws.lScreen.Size[0] + ws.rScreen.Size[0]) ):
		# TODO: Errorクラス
		print 'Error: ワークスペースの幅が左右ディスプレイの幅の合計より小さいです。', ws.Size[0], ws.lScreen.Size[0], ws.rScreen.Size[0]
		return False
	if ( ws.Size[1] > ws.lScreen.Size[1] ):
		print 'Warning: 左ディスプレイの高さがワークスペースに対して低いです。', ws.lScreen.Size[1]
	elif ( ws.Size[1] > ws.rScreen.Size[1] ):
		print 'Warning: 右ディスプレイの高さがワークスペースに対して低いです。', ws.rScreen.Size[1]
	else:
		pass

if __name__ == "__main__":
	ConfigSetting()
