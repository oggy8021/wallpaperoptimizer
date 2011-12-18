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
# $ killall wallpaperoptimizerApplet


#<root> = /usr/local/bin
#		WallpaperOptimizer/
#			Imaging/
#				Bounds.py
#				ImgFile.py
#				Rectangle.py
#				__init__.py
#			glade/
#				wallpositapplet.glade
#			Applet.py
#			ChangerDir.py
#			Config.py
#			Core.py
#			Options.py
#			OptionBase.py
#			WorkSpace.py
#			__init__.py
#		wallpaperoptimizer
#		wallpaperoptimizerApplet
#		setup.py

__NAME__='wallpaperoptimizer'
__VERSION__='0.1.0.0'

params = {
	'name': __NAME__,
	'version': __VERSION__,
	'description': 'wallpaperoptimizer is multi wallpaper changer.',
	'author': 'Katsuhiro Ogikubo',
	'author_email': 'oggyist@gmail.com',
	'url': 'http://oggy.no-ip.info/blog/',
	'scripts': ['wallpaperoptimizer','wallpaperoptimizerApplet'],
	'packages': ['WallpaperOptimizer', 'WallpaperOptimizer/Imaging'],
	'package_dir': {'WallpaperOptimizer': 'WallpaperOptimizer'},
	'package_data': {'WallpaperOptimizer': ['glade/wallpositapplet.glade', 'wallopt.png', 'wallopt_off.png']},
	'data_files': [
		('lib/bonobo/servers',
			['wallpaperoptimizer.server'])],
	'license': 'GPL3',
#	'download_url': 'http://oggy.no-ip.info/blog/wallpaperoptimizer-%s.tar.gz' % (__VERSION__),
	'classifiers': [
		'Intended Audience :: End Users/Desktop',
		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python']
}

import sys
import os
import os.path
from shutil import rmtree
from distutils.core import setup
from distutils.sysconfig import PREFIX, EXEC_PREFIX, get_python_lib
from distutils.debug import DEBUG

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
	if sys.argv[1] == 'install':
		print "*** install action."
		setup(**params)

	elif sys.argv[1] == 'uninstall':
		print "*** uninstall action."
		rmfile(PREFIX + '/bin/' + params['scripts'][0])
		rmfile(PREFIX + '/bin/' + params['scripts'][1])
		rmdir(get_python_lib() + '/' + params['packages'][0])
		rmfile(PREFIX + '/' + params['data_files'][0][0] + '/' + params['data_files'][0][1][0])

#	else:
#		pass
#		PREFIX='/usr/local'
#		print PREFIX
#		print EXEC_PREFIX
#		print get_python_lib()
#		print params['package_data']
#		print params['data_files'][0][0]
#		print params['data_files'][0][1][0]
#		print params['scripts'][0]
#		print params['scripts'][1]
