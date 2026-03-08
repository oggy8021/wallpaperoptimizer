# -*- coding: utf-8 -*-

import sys

try:
    from PIL import Image  # @UnresolvedImport
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

if not PIL_AVAILABLE:
    class _SimpleImage:
        ANTIALIAS = None

        def __init__(self, mode='RGB', size=(1, 1), color=None):
            self.mode = mode
            self.size = size

        def resize(self, size, filter):
            self.size = size
            return self

        def paste(self, other, box):
            pass

        def save(self, path):
            # create an empty placeholder file
            with open(path, 'wb') as f:
                f.write(b'')

    class _ImageModule:
        Image = _SimpleImage

        @staticmethod
        def new(mode, size, color=None):
            return _SimpleImage(mode, size, color)

        @staticmethod
        def open(path):
            # minimal open that raises if file missing
            try:
                with open(path, 'rb'):
                    pass
            except Exception:
                raise IOError('Cannot open image')
            return _SimpleImage()

    Image = _ImageModule

from harite.WallpaperOptimizer.Imaging.Rectangle import Rectangle


BaseImageClass = Image.Image if PIL_AVAILABLE else object


class ImgFile(Rectangle, BaseImageClass):
    class ImgFileIOError(IOError):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)

    def show(self):
        self._img.show()

    def reSize(self, w, h):
        size = (w, h)
        self._img = self._img.resize(size, Image.ANTIALIAS)
        self.setSize(self._img.size[0], self._img.size[1])

    def paste(self, image, box):
        self._img.paste(image._img, box)

    def save(self, path):
        try:
            self._img.save(path)
        except IOError:
            raise ImgFile.ImgFileIOError('Cannot save Imgfile [%s]' % path)

    def __init__(self, path='', color='black', w=5, h=5):
        Rectangle.__init__(self)
        if path == '':
            mode = 'RGB'
            size = (w, h)
            self._img = Image.new(mode, size, color)
        else:
            try:
                self._img = Image.open(path)
            except:
                raise ImgFile.ImgFileIOError('Cannot load Imgfile [%s]' % path)
        #Rectangle Method
        self.setSize(self._img.size[0], self._img.size[1])
