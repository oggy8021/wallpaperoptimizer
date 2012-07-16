# -*- coding: utf-8 -*-

""" WallpaperOptimizer::Core

wallpaperoptimizer core module.
"""

import sys
import os.path
import logging
import subprocess
import time
import datetime
import glob

from WallpaperOptimizer.Config import Config
from WallpaperOptimizer.WorkSpace import WorkSpace
from WallpaperOptimizer.ChangerDir import ChangerDir
from WallpaperOptimizer.Imaging.ImgFile import ImgFile


class Core(object):

	class CoreRuntimeError(Exception):
		def __init__(self, value):
			self.value = value
		def __str__(self):
			return repr(self.value)

	def _initializeConfig(self):
		"""
		config instance set from configfile or instance default.
		"""
		# config set from configfile
		self.configfile = '~/.walloptrc'
		self.configfile = os.path.expanduser(self.configfile)
		if os.path.exists(self.configfile):
			try:
				self.config = Config(self.configfile)
				logging.info('Config set from configfile.')
			except Config.FormatError, msg:
				logging.error('** FormatError: %s. ' % msg)
				raise Core.CoreRuntimeError(msg.value)
		else:
			self.config = Config()

		# config set/update from commandline option
		if (self.option.getLSize() <> None and self.option.getRSize() <> None):
			self.config.lDisplay.toIntAsSizeString(self.option.getLSize())
			self.config.rDisplay.toIntAsSizeString(self.option.getRSize())
			logging.info('Config "display" update from commandline option.')

		if (self.option.getLSrcdir() <> '' and self.option.getRSrcdir() <> ''):
			self.config.lDisplay.setSrcdir(self.option.getLSrcdir())
			self.config.rDisplay.setSrcdir(self.option.getRSrcdir())
			logging.info('Config "srcdir" update from commandline option.')

		if ( not self.option.getWindow() and
			self.config.lDisplay.width == 0 and 
			self.config.lDisplay.height == 0 and
			self.config.rDisplay.width == 0 and 
			self.config.rDisplay.height == 0 ):
			logging.error('** Please setting left/right display size.')
			raise Core.CoreRuntimeError('No setting left/right display size.')

		if ( self.option.getDaemonize() and 
				not self.option.getWindow() and
				self.config.lDisplay.srcdir == '' and 
				self.config.rDisplay.srcdir == '' ):
			logging.error('** Please setting srcdir in Daemonize mode.')
			raise Core.CoreRuntimeError('No setting srcdir ind Daemonize mode.')

		logging.debug('%20s [%d,%d]'
				 % ( 'left display size'
				 , self.config.lDisplay.width
				 , self.config.lDisplay.height ))
		logging.debug('%20s [%d,%d]'
				 % ( 'right display size'
				 , self.config.rDisplay.width
				 , self.config.rDisplay.height ))
		logging.debug('%20s [%s,%s]'
				 % ( 'position'
				 , self.config.lDisplay.posit
				 , self.config.rDisplay.posit ))
		logging.debug('%20s [%s]'
				 % ( 'srcdir to left'
				 , self.config.lDisplay.srcdir ))
		logging.debug('%20s [%s]'
				 % ( 'srcdir to right'
				 , self.config.rDisplay.srcdir ))


	def _initializeWorkSpace(self):
		"""
		WorkSpace instance and Screen instance initialize and compared Screen size.
		"""
		try:
			self.Ws = WorkSpace()
		except WorkSpace.WorkSpaceRuntimeError, msg:
			logging.error('** WorkSpaceRuntimeError: %s. ' % msg)
			raise Core.CoreRuntimeError(msg.value)

		logging.info('Current WorkSpace setting as.')
		logging.debug('%20s [%d,%d]'
			 % ( 'WorkSpace Size', self.Ws.Size.w, self.Ws.Size.h ))
		logging.debug('%20s [%s]'
			 % ( 'WorkSpace depth', self.Ws.getDepth() ))

		logging.debug('Config Setting To WorkSpace().')

		self.Ws.setScreenSize((self.config.lDisplay.width
								, self.config.lDisplay.height)
								, (self.config.rDisplay.width
								, self.config.rDisplay.height))
		self.Ws.setBool(self.config.lDisplay.getBool(), self.config.rDisplay.getBool())

		if not self.Ws.compareToScreen():
			logging.error(
				'** WorkSpace width[%d] < sum(left display size, right display size) [%d, %d].'
				 % ( self.Ws.Size.w, self.Ws.lScreen.Size.w, self.Ws.rScreen.Size.w ))
			raise Core.CoreRuntimeError('WorkSpace width over left/right display size summing')

		if (hasattr(self.Ws.lScreen.Size, 'islessThanWorkSpaceHeight')
		 and self.Ws.lScreen.Size.islessThanWorkSpaceHeight):
			logging.warning(
				'* WorkSpace height [%s] > left display height [%s].'
				 % (self.Ws.Size.h, self.Ws.lScreen.Size.h ))
		if (hasattr(self.Ws.rScreen.Size, 'islessThanWorkSpaceHeight')
		 and self.Ws.rScreen.Size.islessThanWorkSpaceHeight):
			logging.warning(
				'* WorkSpace height [%s] > right display height [%s].'
				 % (self.Ws.Size.h, self.Ws.rScreen.Size.h ))

		self.Ws.setAttrScreenType()


		if (hasattr(self.Ws.lScreen, 'displayType')):
			tmpDisplayType1 = self.Ws.lScreen.displayType
		else:
			tmpDisplayType1 = "undefined"
		if (hasattr(self.Ws.rScreen, 'displayType')):
			tmpDisplayType2 = self.Ws.rScreen.displayType
		else:
			tmpDisplayType2 = "undefined"

		logging.debug('%20s [%s,%s]'
			 	 % ( 'display type' , tmpDisplayType1, tmpDisplayType2))


	def _checkImgType(self, Ws, Img1, Img2):
		"""
		ImgFile square type decide by aspectratio.
		"""
		logging.info('Checking imgType as Imgfile.')

		if ( Img1.Size.w < Ws.lScreen.Size.w or Img1.Size.w < Ws.rScreen.Size.w ):
			if Img1.isDual():
				setattr(Img1, 'imgType', 'dual')
		if ( Img2.Size.w < Ws.lScreen.Size.w or Img2.Size.w < Ws.rScreen.Size.w ):
			if Img2.isDual():
				setattr(Img2, 'imgType', 'dual')

		if Img1.isSquare():
			setattr(Img1, 'imgType', 'square')
		if Img1.isWide():
			setattr(Img1, 'imgType', 'wide')

		if Img2.isSquare():
			setattr(Img2, 'imgType', 'square')
		if Img2.isWide():
			setattr(Img2, 'imgType', 'wide')

		if not hasattr(Img1, 'imgType'):
			setattr(Img1, 'imgType', 'other')
		if not hasattr(Img2, 'imgType'):
			setattr(Img2, 'imgType', 'other')

		logging.debug('%20s [%s]' % ( 'imgType as Img1', Img1.imgType) )
		logging.debug('%20s [%s]' % ( 'imgType as Img2', Img2.imgType) )


	def _bindingImgToScreen(self, Fixed, Img1, Img2):
		"""
		ImgFile is binding to Screen instance.
		"""
#! 		組み合わせバリエーションに対応しきれているか、見極められていない
		logging.info('Binding Img to Screen.')

		if Fixed:
			setattr(Img1, 'posit', 'left')
			logging.debug('%20s [%s]' % ( 'Img1 fixed binding', Img1.posit) )
			setattr(Img2, 'posit', 'right')
			logging.debug('%20s [%s]' % ( 'Img2 fixed binding', Img2.posit) )
		else:
			# アスペクト比見て、ディスプレイのタイプに応じて優先的に割り当てる
			if Img1.imgType == Ws.lScreen.displayType:
				setattr(Img1, 'posit', 'left')
				logging.debug('%20s [%s]' % ( 'Img1 binding', Img1.posit) )
				setattr(Img2, 'posit', 'right')
				logging.debug('%20s [%s]' % ( 'Img2 binding', Img2.posit) )
			elif Img1.imgType == Ws.rScreen.displayType:
				setattr(Img1, 'posit', 'right')
				logging.debug('%20s [%s]' % ( 'Img1 binding', Img1.posit) )
				setattr(Img2, 'posit', 'left')
				logging.debug('%20s [%s]' % ( 'Img2 binding', Img2.posit) )
			else:
				setattr(Img1, 'posit', 'left')
				logging.debug('%20s [%s]' % ( 'Img1 binding', Img1.posit) )
				setattr(Img2, 'posit', 'right')
				logging.debug('%20s [%s]' % ( 'Img2 binding', Img2.posit) )


	def _checkContain(self, Ws, Img, tmpMergin):
		"""
		ImgFile check that contains Screen.
		"""
		logging.info('Check Imgfile contain %s Screen.' % Img.posit)

		if Img.posit == 'left':
			# lScreenに、Imgがおさまる
			if ( Ws.lScreen.containsPlusMergin( Img, tmpMergin) ):
				return True
			else:
				return False
		elif Img.posit == 'right':
			# rScreenに、Imgがおさまる
			if ( Ws.rScreen.containsPlusMergin( Img, tmpMergin) ):
				return True
			else:
				return False


	def _downsizeImg(self, Ws, Img, tmpMergin):
		"""
		ImgFile is fitting to Screen size.
		"""
		if Img.posit == 'left':
			tmpScreen = Ws.lScreen
		elif Img.posit == 'right':
			tmpScreen = Ws.rScreen
		logging.info('Convert Imgfile with %s Screen.' % Img.posit)

		tmpMerginW = tmpMergin[0] + tmpMergin[1]
		logging.debug('%20s [%s]' % ( 'width mergin', tmpMerginW) )
		tmpMerginH = tmpMergin[2] + tmpMergin[3]
		logging.debug('%20s [%s]' % ( 'height mergin', tmpMerginH) )

		if Img.Size.w > tmpScreen.Size.w:
			Img.setSize( (tmpScreen.Size.w - tmpMerginW), 
					int(max( Img.Size.h
					 * (tmpScreen.Size.w - tmpMerginW) / Img.Size.w, 1 )) )
		if Img.Size.h > tmpScreen.Size.h:
			Img.setSize( int(max( Img.Size.w
					 * (tmpScreen.Size.h - tmpMerginH) / Img.Size.h , 1 )), 
					(tmpScreen.Size.h - tmpMerginH) )

		Img.reSize( Img.Size.w, Img.Size.h)
		logging.debug('%20s [%d,%d]' % ( 'converted size', Img.Size.w, Img.Size.h) )


	def _allocateCenter(self, Ws, Img1, Img2):
		"""
		ImgFile and Screen calculate center position.
		"""
		logging.info('Calculate center position.')

		Ws.lScreen.calcCenter()
		Ws.rScreen.calcCenter()
		Img1.calcCenter()
		Img2.calcCenter()

		logging.debug('%20s [%d,%d]'
			 % ( 'left screen', Ws.lScreen.center.x, Ws.lScreen.center.y) )
		if Img1.posit == 'left':
			logging.debug('%20s [%d,%d]' % ( 'Img1', Img1.center.x, Img1.center.y) )
		else:
			logging.debug('%20s [%d,%d]' % ( 'Img2', Img2.center.x, Img2.center.y) )

		logging.debug('%20s [%d,%d]'
			 % ( 'right screen', Ws.rScreen.center.x, Ws.rScreen.center.y) )
		if Img1.posit == 'right':
			logging.debug('%20s [%d,%d]' % ( 'Img1', Img1.center.x, Img1.center.y) )
		else:
			logging.debug('%20s [%d,%d]' % ( 'Img2', Img2.center.x, Img2.center.y) )


	def _allocateImg(self, Option, Ws, Img):
		"""
		ImgFile calculate allocate position.
		"""
		if Img.posit == 'left':
			tmpScreen = Ws.lScreen
			tmpAlign = Option.getLAlign()
			tmpValign = Option.getLValign()
		elif Img.posit == 'right':
			tmpScreen = Ws.rScreen
			tmpAlign = Option.getRAlign()
			tmpValign = Option.getRValign()
		logging.info('Allocate Imgfile to %s Screen.' % Img.posit)

		# 画面中央と画像中央との距離をタプルで得る
		centerDistance = (abs( Img.center.distanceX(tmpScreen.center) ) 
			, abs( Img.center.distanceY(tmpScreen.center) ) )
		rightcornerDistance = (abs( Img.end.distanceX(tmpScreen.end) )
			 , abs( Img.end.distanceY(tmpScreen.end) ) )

		# Imgはインスタンス化されたときに、x,y = 0,0 つまり align=left, valign=top
		if tmpAlign == 'center':
			if Img.center.x <> tmpScreen.center.x:
				Img.start.x += centerDistance[0]
				Img.end.x += centerDistance[0]
		elif tmpAlign == 'right':
			if Img.end.x <> tmpScreen.end.x:
				Img.start.x += rightcornerDistance[0]
				Img.end.x += rightcornerDistance[0]

		if tmpValign == 'middle':
			if Img.center.y <> tmpScreen.center.y:
				Img.start.y += centerDistance[1]
				Img.end.y += centerDistance[1]
		elif tmpValign == 'bottom':
			if Img.end.y <> tmpScreen.end.y:
				Img.start.y += rightcornerDistance[1]
				Img.end.y += rightcornerDistance[1]

		logging.debug('%20s [%d,%d]' % ( 'start', Img.start.x, Img.start.y) )
		logging.debug('%20s [%d,%d]' % ( 'end', Img.end.x, Img.end.y) )


	def _mergeWallpaper(self, Ws, bkImg, Img):
		"""
		ImgFile paste to Wallpaper Img.
		"""
		logging.info('Merge Imgfile to %s Screen.' % Img.posit)

		if Img.posit == 'right':
			Img.start.x += Ws.lScreen.Size.w
			Img.end.x += Ws.lScreen.Size.w
			# center.x
		bkImg.paste( Img, (Img.start.x, Img.start.y, Img.end.x, Img.end.y) )


	def _optimizeWallpaper(self, Option, Config, Ws, Img1, Img2):
		"""
		2 ImgFile allocate Wallpaper Img.
		"""
		logging.info('Optimizing ... wallpapaer.')
		self._checkImgType(Ws, Img1, Img2)

		self._bindingImgToScreen(Option.getFixed, Img1, Img2)

		logging.info('Calculate mergin.')
		lMergin = (Option.getLMergin(), 0, Option.getTopMergin(), Option.getBtmMergin())
		logging.debug('%20s [%d,%d,%d,%d]'
				 % ( 'left Screen mergin', lMergin[0], lMergin[1], lMergin[2], lMergin[3] ))
		rMergin = (0, Option.getRMergin(), Option.getTopMergin(), Option.getBtmMergin())
		logging.debug('%20s [%d,%d,%d,%d]'
				 % ( 'right Screen mergin', rMergin[0], rMergin[1], rMergin[2], rMergin[3] ))
		if self.Ws.lScreen.bSetting and self.Ws.rScreen.bSetting:
			if not self._checkContain(Ws, Img1, lMergin):
				self._downsizeImg(Ws, Img1, lMergin)
			if not self._checkContain(Ws, Img2, rMergin):
				self._downsizeImg(Ws, Img2, rMergin)

			self._allocateCenter(Ws, Img1, Img2)
			self._allocateImg(Option, Ws, Img1)
			self._allocateImg(Option, Ws, Img2)

			bkImg = ImgFile('', Option.getBgcolor(), Ws.Size.w, Ws.Size.h)

			self._mergeWallpaper(Ws, bkImg, Img1)
			self._mergeWallpaper(Ws, bkImg, Img2)
			return bkImg
		elif self.Ws.lScreen.bSetting and not self.Ws.rScreen.bSetting:
			return Img1
		elif not self.Ws.lScreen.bSetting and self.Ws.rScreen.bSetting:
			return Img2


	def _setWall(self, bkImg, tmpPath=None):
		"""
		Wallpaper Img set to GNOME wallpaper.
		"""
		removePath = subprocess.Popen(
				["gconftool-2"
				,"--get"
				,"/desktop/gnome/background/picture_filename"]
				, stdout=subprocess.PIPE).communicate()[0].rstrip()
		logging.debug('Current wallpaper [%s].' % removePath)
		if removePath.find('wallopt') < 0:
			removePath = None

		if tmpPath == None:
			tmpPath = self._saveImgfile(bkImg, tmpPath)

		tmpPath = os.path.abspath(tmpPath)
		ret = subprocess.call(
				["gconftool-2"
				,"--type"
				,"string"
				,"--set"
				,"/desktop/gnome/background/picture_filename"
				,tmpPath])
		retopt = subprocess.call(
				["gconftool-2"
				,"--type"
				,"string"
				,"--set"
				,"/desktop/gnome/background/picture_options"
				,"scaled"])
		logging.info('Change wallpaper to current Workspace [%s].' % (tmpPath))

		if removePath <> None:
			if os.path.exists(removePath):
				os.remove(removePath)
				logging.debug('Delete wallpaper [%s].' % removePath)
			lstCleanFile = glob.glob('/tmp/wallopt*.jpg')
			if len(lstCleanFile) > 1:
				lstCleanFile.remove(tmpPath)
				for x in lstCleanFile:
					os.remove(x)
					logging.debug('Cleanup old wallpapaer [%s].' % x)

	def _saveImgfile(self, bkImg, tmpPath):
		try:
			if tmpPath == None:
				tmpPath = '/tmp/wallopt' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
			bkImg.save(tmpPath)
			logging.info('Save optimized wallpaper [%s].' % tmpPath)
			return tmpPath
		except ImgFile.ImgFileIOError, msg:
			raise Core.CoreRuntimeError(msg.value)


	def timerRun(self):
		try:
			LChangerDir = ChangerDir(self.config.lDisplay.srcdir)
			RChangerDir = ChangerDir(self.config.rDisplay.srcdir)
		except ChangerDir.FileCountZeroError, msg:
			raise Core.CoreRuntimeError(msg.value)

		Img1 = ImgFile(LChangerDir.getImgfileRnd())
		Img2 = ImgFile(RChangerDir.getImgfileRnd())

		bkImg = self._optimizeWallpaper(self.option, self.config, self.Ws, Img1, Img2)
		self._setWall(bkImg)


	def background(self):
		try:
			LChangerDir = ChangerDir(self.config.lDisplay.srcdir)
			RChangerDir = ChangerDir(self.config.rDisplay.srcdir)
		except ChangerDir.FileCountZeroError, msg:
			logging.error('** %s.' % msg)
			sys.exit(2)

		try:
			while(1):
				try:
					Img1 = ImgFile(LChangerDir.getImgfileRnd())
					Img2 = ImgFile(RChangerDir.getImgfileRnd())
				except ImgFile.ImgFileIOError, msg:
					raise Core.CoreRuntimeError(msg.value)

				bkImg = self._optimizeWallpaper(self.option, self.config, self.Ws, Img1, Img2)
				self._setWall(bkImg)
				interval = self.option.getInterval()
				time.sleep(interval)
		except KeyboardInterrupt:
			sys.exit(0)

	def _loadImgFile(self, path):
		if path <> '':
			try:
				Img = ImgFile(path)
			except ImgFile.ImgFileIOError, msg:
					raise Core.CoreRuntimeError(msg.value)
			logging.info('Create Img object. [%s]' % path)
			logging.debug('%20s [%d,%d]' % ( 'Img', Img.Size.w, Img.Size.h ))
			return Img
		else:
			try:
				dummyImg = ImgFile('', self.option.getBgcolor())
			except ImgFile.ImgFileIOError, msg:
					raise Core.CoreRuntimeError(msg.value)
			logging.debug('Create Dummy Img object.')
			return dummyImg

	def singlerun(self):
		if (self.option.lengthArgs() == 2 or 
			( self.option.lengthArgs() == 1 and
			 not self.option.getCombine() )):
			Imgs = (self._loadImgFile(self.option.getLArg()), self._loadImgFile(self.option.getRArg()))
			bkImg = self._optimizeWallpaper(self.option, self.config, self.Ws, Imgs[0], Imgs[1])
			tmpPath = self.option.getSavePath()
			if tmpPath <> None:
				self._saveImgfile(bkImg, tmpPath)
			if self.option.getSetWall():
				self._setWall(bkImg, tmpPath)

		elif self.option.lengthArgs() == 1 and self.option.getCombine():
			if self.option.getSetWall():
				if self.option.getLArg() <> '':
					self._setWall(None, self.option.getLArg())
				else:
					self._setWall(None, self.option.getRArg())

	def __init__(self, Options):
		self.option = Options
		self._initializeConfig()
		self._initializeWorkSpace()
