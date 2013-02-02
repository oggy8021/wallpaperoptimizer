#!/usr/bin/env python
# -*- coding: utf-8 -*-

#<install>
#	sudo paco -D "python ./setup.py install"
#<uninstall>
#	$ python setup.py uninstall
#	 or
#	$ sudo paco -r [name]
#<reinstall>
#	$ sudo python setup.py uninstall ; sudo python setup.py install
#<abort>
# $ killall wallpaperoptimizer

#	/usr/bin
#			wallpaperoptimiz
#	/usr/share
#			wallopt.png
#			wallopt_off.png
#	/usr/lib/python2.4/site-packages
#		WallpaperOptimizer/
#			Imaging/
#				Bounds.py
#				ImgFile.py
#				Rectangle.py
#				__init__.py
#			glade/
#				wallpositapplet.glade
#			Applet.py
#			AppletUtil.py
#			ChangerDir.py
#			Config.py
#			Core.py
#			Options.py
#			OptionBase.py
#			WorkSpace.py
#			__init__.py

__NAME__='wallpaperoptimizer'
__VERSION__='0.6.0.0'

params = {
	'name': __NAME__,
	'version': __VERSION__,
	'description': 'wallpaperoptimizer is multi wallpaper changer.',
	'author': 'Katsuhiro Ogikubo',
	'author_email': 'oggyist@gmail.com',
	'url': 'http://oggy.no-ip.info/blog/',
	'scripts': ['wallpaperoptimiz'],
	'packages': ['WallpaperOptimizer', 'WallpaperOptimizer/Imaging', 'WallpaperOptimizer/Widget'],
	'package_dir': {'WallpaperOptimizer': 'WallpaperOptimizer'},
	'package_data': {'WallpaperOptimizer': ['glade/wallpositapplet.glade']},
	'license': 'GPL3',
#	'download_url': 'http://oggy.no-ip.info/blog/wallpaperoptimizer-%s.tar.gz' % (__VERSION__),
	'classifiers': [
		'Intended Audience :: End Users/Desktop',
		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python']
}

import sys, platform
import os.path
from shutil import rmtree
from setuptools import setup
from distutils.sysconfig import PREFIX, get_python_lib

def rmfile(path):
	if os.path.exists(path):
		os.remove(path)
		print "  remove file: %s" % path
	else:
		print "  already removed: %s" % path

def rmdir(path):
	if os.path.exists(path):
		rmtree(path)
		print "  remove dirs: %s" % path
	else:
		print "  already removed: %s" % path


if __name__ == "__main__":
	print "*** %s action." % sys.argv[1]
	if os.uname()[4] == 'x86_64':
		params['data_files'] = [
			('share/WallpaperOptimizer',
				['wallopt.png', 'wallopt_off.png']),
			('/etc/logrotate.d',
				['wallopt'])]
		bonobo = ('lib64/bonobo/servers',	['wallpaperoptimizer.server'])
	else:
		params['data_files'] = [
			('share/WallpaperOptimizer',
				['wallopt.png', 'wallopt_off.png']),
			('/etc/logrotate.d',
				['wallopt'])]
		bonobo = ('lib/bonobo/servers',	['wallpaperoptimizer.server'])

	if platform.linux_distribution()[0] in ('CentOS','Red Hat Linux'):
		param['data_files'].append(bonobo)


	if sys.argv[1] == 'uninstall':
		rmfile(os.path.join(PREFIX,'bin',params['scripts'][0]))
		rmdir(os.path.join(get_python_lib(),params['packages'][0]))
		rmdir(os.path.join(PREFIX,params['data_files'][0][0]))
		rmfile(os.path.join(params['data_files'][1][0],params['data_files'][1][1][0]))
		rmfile(os.path.join(PREFIX,params['data_files'][2][0],params['data_files'][2][1][0]))
	else:
		setup(**params)


#	elif sys.argv[1] == 'dump':
#		print type(params)
#		print params['data_files']
