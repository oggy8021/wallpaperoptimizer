# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_

from WallpaperOptimizer.Imaging.ImgFile import ImgFile

import os.path


def ImgFile_init_no_param_test():
    Img = ImgFile()
    eq_(Img.getSize().w, 5)
    eq_(Img.getSize().h, 5)


def ImgFile_load_square_test():
    file = '~/Develop/WallPosit.git/2560x1920.jpg'  # 4:3
    Img = ImgFile(os.path.expanduser(file))
    eq_(Img.getSize().w, 2560)
    eq_(Img.getSize().h, 1920)
    ok_(Img.isSquare())
    ok_(not Img.isWide())
    ok_(not Img.isDual())
    Img.calcCenter()
    eq_(Img.getCenter().x, 1280)
    eq_(Img.getCenter().y, 960)


def ImgFile_load_wide_test():
    file = '~/Develop/WallPosit.git/1500x844.jpg'   # 16:9
    Img = ImgFile(os.path.expanduser(file))
    eq_(Img.getSize().w, 1500)
    eq_(Img.getSize().h, 844)
    ok_(Img.isWide())
    ok_(not Img.isSquare())
    ok_(not Img.isDual())


def ImgFile_load_dual_test():
    file = '~/Develop/WallPosit.git/3200x1080.jpg'  # 8:2.7
    Img = ImgFile(os.path.expanduser(file))
    eq_(Img.getSize().w, 3200)
    eq_(Img.getSize().h, 1080)
    ok_(Img.isDual())
    ok_(not Img.isSquare())
    ok_(not Img.isWide())


def ImgFile_load_no_match_test():
    file = '~/Develop/WallPosit.git/1000x800.jpg'   # No Match
    Img = ImgFile(os.path.expanduser(file))
    eq_(Img.getSize().w, 1000)
    eq_(Img.getSize().h, 800)
    ok_(Img.isSquare())
    ok_(not Img.isWide())
    ok_(not Img.isDual())


def ImgFile_reSize_test():
    file = '~/Develop/WallPosit.git/1000x800.jpg'   # No Match
    Img = ImgFile(os.path.expanduser(file))
    Img.reSize(500, 400)
    eq_(Img.getSize().w, 500)
    eq_(Img.getSize().h, 400)


def ImgFile_paste_test():
    Img1 = ImgFile('', 'black', 1000, 800)
    Img2 = ImgFile('', 'black', 1000, 800)
    Img3 = ImgFile('', 'white', 500, 400)
    Img3.start.x = 20
    Img3.start.y = 16
    Img3.end.x += Img3.start.x
    Img3.end.y += Img3.start.y
    box1 = (Img3.start.x, Img3.start.y)
    box2 = (Img3.start.x, Img3.start.y, Img3.end.x, Img3.end.y)
    Img1.paste(Img3, box1)
    Img2.paste(Img3, box2)
#	毎回保存しちゃうから止めてある
#	Img1.save('walltest1.jpg')
#	Img2.save('walltest2.jpg')
