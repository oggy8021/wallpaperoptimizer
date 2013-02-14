# -*- coding: utf-8 -*-

from WallpaperOptimizer.Core import Core

class Starter(object):

    def _runConsoleSide(self, option, logging):
        if option.getVerbose():
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)
            _putlogOption(option)
    
        if option.getDaemonize():
            core = Core(option)
            logging.debug('Running ... daemonize mode.')
            try:
                core.background()
            except Core.CoreRuntimeError, msg:
                logging.error('** CoreRuntimeError: %s. ' % msg.value)
                sys.exit(2)
        else:
            core = Core(option)
            logging.debug('Running ... singlerun mode.')
            try:
                core.singlerun()
            except Core.CoreRuntimeError, msg:
                logging.error('** CoreRuntimeError: %s. ' % msg.value)
                sys.exit(2)

    def start(self):
        pass