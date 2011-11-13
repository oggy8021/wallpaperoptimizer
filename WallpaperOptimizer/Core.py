# -*- coding: utf-8 -*-

import sys
import os.path
import time
import logging
import subprocess

from WallpaperOptimizer.ChangerDir import ChangerDir
from WallpaperOptimizer.Imaging.ImgFile import ImgFile


class Core(object):

	def checkImgType(self, Ws, Img1, Img2):
		self.logging.debug('Checking imgType as Imgfile.')

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

		self.logging.debug('%20s [%s]' % ( 'imgType as Img1', Img1.imgType) )
		self.logging.debug('%20s [%s]' % ( 'imgType as Img2', Img2.imgType) )


	def bindingImgToScreen(self, Fixed, Img1, Img2):
		# バリエーションに対応できているか、見極められていない
		self.logging.debug('Binding Img to Screen.')

		if ( Fixed ):
			setattr(Img1, 'posit', 'left')
			self.logging.debug('%20s [%s]' % ( 'Img1 fixed binding', Img1.posit) )
			setattr(Img2, 'posit', 'right')
			self.logging.debug('%20s [%s]' % ( 'Img2 fixed binding', Img2.posit) )
		else:
			# アスペクト比見て、ディスプレイのタイプに応じて優先的に割り当てる
			if ( Img1.imgType == Ws.lScreen.displayType ):
				setattr(Img1, 'posit', 'left')
				self.logging.debug('%20s [%s]' % ( 'Img1 binding', Img1.posit) )
				setattr(Img2, 'posit', 'right')
				self.logging.debug('%20s [%s]' % ( 'Img2 binding', Img2.posit) )
			elif ( Img1.imgType == Ws.rScreen.displayType ):
				setattr(Img1, 'posit', 'right')
				self.logging.debug('%20s [%s]' % ( 'Img1 binding', Img1.posit) )
				setattr(Img2, 'posit', 'left')
				self.logging.debug('%20s [%s]' % ( 'Img2 binding', Img2.posit) )
			else:
				setattr(Img1, 'posit', 'left')
				self.logging.debug('%20s [%s]' % ( 'Img1 binding', Img1.posit) )
				setattr(Img2, 'posit', 'right')
				self.logging.debug('%20s [%s]' % ( 'Img2 binding', Img2.posit) )


	def checkContain(self, Ws, Img, tmpMergin):
		self.logging.debug('Check Imgfile contain %s Screen.' % Img.posit)

		if ( Img.posit == 'left' ):
			# lScreenに、Imgがおさまる
			if ( Ws.lScreen.containsPlusMergin( Img, tmpMergin) ):
				return True
			else:
				return False
		elif ( Img.posit == 'right' ):
			# rScreenに、Imgがおさまる
			if ( Ws.rScreen.containsPlusMergin( Img, tmpMergin) ):
				return True
			else:
				return False


	def downsizeImg(self, Ws, Img, tmpMergin):
		if ( Img.posit == 'left' ):
			tmpScreen = Ws.lScreen
		elif ( Img.posit == 'right' ):
			tmpScreen = Ws.rScreen
		self.logging.debug('Convert Imgfile with %s Screen.' % Img.posit)

		tmpMerginW = tmpMergin[0] + tmpMergin[1]
		self.logging.debug('%20s [%s]' % ( 'width mergin', tmpMerginW) )
		tmpMerginH = tmpMergin[2] + tmpMergin[3]
		self.logging.debug('%20s [%s]' % ( 'height mergin', tmpMerginH) )

		if ( Img.getSize().w > tmpScreen.getSize().w ):
			Img.setSize( (tmpScreen.getSize().w - tmpMerginW), 
					int(max( Img.getSize().h
					 * (tmpScreen.getSize().w - tmpMerginW) / Img.getSize().w, 1 )) )
		if ( Img.getSize().h > tmpScreen.getSize().h ):
			Img.setSize( int(max( Img.getSize().w
					 * (tmpScreen.getSize().h - tmpMerginH) / Img.getSize().h , 1 )), 
					(tmpScreen.getSize().h - tmpMerginH) )

		Img.reSize( Img.getSize().w, Img.getSize().h)
		self.logging.debug('%20s [%d,%d]' % ( 'converted size', Img.getSize().w, Img.getSize().h) )


	def allocateInit(self, Ws, Img1, Img2):
		self.logging.debug('Calculate center position.')

		Ws.lScreen.calcCenter()
		Ws.rScreen.calcCenter()
		Img1.calcCenter()
		Img2.calcCenter()

		self.logging.debug('%20s [%d,%d]'
			 % ( 'left screen', Ws.lScreen.center.x, Ws.lScreen.center.y) )
		if (Img1.posit == 'left'):
			self.logging.debug('%20s [%d,%d]' % ( 'Img1', Img1.center.x, Img1.center.y) )
		else:
			self.logging.debug('%20s [%d,%d]' % ( 'Img2', Img2.center.x, Img2.center.y) )

		self.logging.debug('%20s [%d,%d]'
			 % ( 'right screen', Ws.rScreen.center.x, Ws.rScreen.center.y) )
		if (Img1.posit == 'right'):
			self.logging.debug('%20s [%d,%d]' % ( 'Img1', Img1.center.x, Img1.center.y) )
		else:
			self.logging.debug('%20s [%d,%d]' % ( 'Img2', Img2.center.x, Img2.center.y) )


	def allocateImg(self, Option, Ws, Img):
		if ( Img.posit == 'left'):
			tmpScreen = Ws.lScreen
			tmpAlign = Option.getLAlign()
			tmpValign = Option.getLValign()
		elif ( Img.posit == 'right'):
			tmpScreen = Ws.rScreen
			tmpAlign = Option.getRAlign()
			tmpValign = Option.getRValign()
		self.logging.debug('Allocate Imgfile to %s Screen.' % Img.posit)

		# 画面中央と画像中央との距離をタプルで得る
		centerDistance = (abs( Img.center.distanceX(tmpScreen.center) ) 
			, abs( Img.center.distanceY(tmpScreen.center) ) )
		rightcornerDistance = (abs( Img.end.distanceX(tmpScreen.end) )
			 , abs( Img.end.distanceY(tmpScreen.end) ) )

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

		self.logging.debug('%20s [%d,%d]' % ( 'start', Img.start.x, Img.start.y) )
		self.logging.debug('%20s [%d,%d]' % ( 'end', Img.end.x, Img.end.y) )


	def mergeWallpaper(self, Ws, bkImg, Img):
		self.logging.debug('Merge Imgfile to %s Screen.' % Img.posit)

		if (Img.posit == 'right'):
			Img.start.x += Ws.lScreen.Size.w
			Img.end.x += Ws.lScreen.Size.w
			# center.x
		bkImg.paste( Img, (Img.start.x, Img.start.y, Img.end.x, Img.end.y) )


	def optimizeWallpaper(self, Option, Config, Ws, Img1, Img2):
		self.logging.debug('Optimizing ... wallpapaer.')
		self.checkImgType(Ws, Img1, Img2)

		self.bindingImgToScreen(Option.getFixed, Img1, Img2)

		self.logging.debug('Calculate mergin.')
		lMergin = [Option.getLMergin(), 0, Option.getTopMergin(), Option.getBtmMergin()]
		self.logging.debug('%20s [%d,%d,%d,%d]'
				 % ( 'left display mergin', lMergin[0], lMergin[1], lMergin[2], lMergin[3] ))
		rMergin = [0, Option.getRMergin(), Option.getTopMergin(), Option.getBtmMergin()]
		self.logging.debug('%20s [%d,%d,%d,%d]'
				 % ( 'right display mergin', rMergin[0], rMergin[1], rMergin[2], rMergin[3] ))

		if (not self.checkContain(Ws, Img1, lMergin)):
			self.downsizeImg(Ws, Img1, lMergin)
		if (not self.checkContain(Ws, Img2, rMergin)):
			self.downsizeImg(Ws, Img2, rMergin)

		self.allocateInit(Ws, Img1, Img2)
		self.allocateImg(Option, Ws, Img1)
		self.allocateImg(Option, Ws, Img2)

		bkImg = ImgFile('', Ws.Size.w, Ws.Size.h, Option.getBgcolor())

		self.mergeWallpaper(Ws, bkImg, Img1)
		self.mergeWallpaper(Ws, bkImg, Img2)

		return bkImg


	def setWall(self, bkImg, tmpPath=None, flg='_setWall'):
		if (tmpPath == None):
			tmpPath = '/tmp/wallposit' + str(flg) + '.jpg'
			bkImg.save(tmpPath)
			self.logging.debug('Save optimized wallpaper [%s].' % tmpPath)
		else:
			# (, )だけだと、ちょっと間抜け
			tmpPath = tmpPath.replace('(','\\(')
			tmpPath = tmpPath.replace(')','\\)')

		tmpPath = os.path.abspath(tmpPath)
		ret = subprocess.call(
				["gconftool-2"
				,"--type"
				,"string"
				,"--set"
				,"/desktop/gnome/background/picture_filename"
				,tmpPath])
		self.logging.debug('Change wallpaper to current Workspace [%s].' % tmpPath)


	def timerRun(self, Option, Config, Ws, i):
		LChangerDir = ChangerDir(Config.lDisplay.getConfig()['srcdir'])
		RChangerDir = ChangerDir(Config.rDisplay.getConfig()['srcdir'])

		Img1 = ImgFile(LChangerDir.getImgfileRnd())
		Img2 = ImgFile(RChangerDir.getImgfileRnd())

		bkImg = self.optimizeWallpaper(Option, Config, Ws, Img1, Img2)
		if (i == 1):
			i = 2
		else:
			i = 1
		self.setWall(bkImg, None, i)
		return i


	def background(self, Option, Config, Ws):
		LChangerDir = ChangerDir(Config.lDisplay.getConfig()['srcdir'])
		RChangerDir = ChangerDir(Config.rDisplay.getConfig()['srcdir'])

		try:
			i = 1
			while(1):
				Img1 = ImgFile(LChangerDir.getImgfileRnd())
				Img2 = ImgFile(RChangerDir.getImgfileRnd())

				bkImg = self.optimizeWallpaper(Option, Config, Ws, Img1, Img2)
				if (i > 2):
					i = 1
				self.setWall(bkImg, None, i)
				interval = Option.getInterval()
				time.sleep(interval)
				i += 1
		except KeyboardInterrupt:
			sys.exit(0)


	def singlerun(self, Option, Config, Ws):
		if len( Option.getArgs() ) == 2:
			Img1 = ImgFile(Option.getLArg())
			self.logging.debug('Create Img1 object. [%s]' % Option.getLArg())
			self.logging.debug('%20s [%d,%d]' % ( 'Img1', Img1.getSize().w, Img1.getSize().h ))
			Img2 = ImgFile(Option.getRArg())
			self.logging.debug('Create Img2 object. [%s]' % Option.getRArg())
			self.logging.debug('%20s [%s,%s]' % ( 'Img2', Img2.getSize().w, Img2.getSize().h ))
			bkImg = self.optimizeWallpaper(Option, Config, Ws, Img1, Img2)

			tmpPath = Option.getSavePath()
			if (tmpPath <> None):
				bkImg.save(tmpPath)
				self.logging.debug('Save optimized wallpaper [%s].' % tmpPath)

			if (Option.getSetWall()):
				self.setWall(bkImg)


	def __init__(self, logger):
		self.logging = logger
