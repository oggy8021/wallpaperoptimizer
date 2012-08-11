
【wallpaper optimizer】
  ～wallpaperoptimizer is wallpaper changer for multi screen.～

													Katsuhiro Ogikubo
													oggyist@gmail.com

1.はじめに
  wallpaper optimizerは、マルチモニタ使用下において壁紙を最適に配置する
  プログラムです。以下の動作モードと機能を備えます。

  ＜動作モード＞
  ・コンソールより各種パラメータを指定して、壁紙を作成・設定
  ・コンソール下にて、指定時間ごとに壁紙を変更
  ・GNOMEパネルに配置するGNOMEアプレットとして動作
    （上記、両機能をGUIより実行可能）

  ＜機能＞
  ・画像２つを指定し、モニタサイズと画像サイズから最適配置を行います
  ・モニタに対しての画像配置を左右モニタごとに、上寄せ・下寄せ（左右）などと指定できます
  ・モニタ端からのマージンを指定できます（ウィジットの配置領域確保などに）
  ・チェンジャーのOn/Offをパネル上から変更できます
  ・壁紙設定は画像１つの指定でも動作
  
  また、以下のような機能は実装できていません。
  ・モニタを回転、縦置きで使用している場合
  ・アプレットモードでのヘルプ


2.インストール
  $ sudo python setup.py install


3.アンインストール
  $ sudo python setup.py uninstall


4.展開ディレクトリ
  setup.pyをご覧ください。
  実行時に、/tmpにログファイルと壁紙ファイル（保存ファイル名を指定しない場合など）を作成します。


5.起動方法
5.1.コンソールでの実行例
  $ wallpaperoptimizer 2560x1920.jpg 1500x844.jpg -C

5.2.コンソールからの壁紙チェンジャー実行例
  $ wallpaperoptimizer -D -i 3600 &

5.3.GNOMEアプレットとしての実行
  GNOMEパネル上の任意箇所で右クリックし、「パネルへ追加」を選択。
  「Wallpaperoptimizer Applet」を選択。


6.使いかた
6.1. コンソール
  ヘルプをご覧ください。
  $ wallpaperoptimizer -h または --help

6.2. アプレット
  最初に起動されるメインウィンドウ内のボタン配置が、モニタを左右に配置したイメージ
  になります。マージンについてはワークスペース全体への指定となります。
  また、メインウィンドウの下に並ぶボタンが各操作ボタンです。ボタンによっては設定を
  行わないと有効にならないものがあります。


7.開発環境
  /etc/redhat-release
	CentOS release 6.3
  uname -r
	2.6.32-279.1.1.el6.centos.plus.x86_64
  関連してそうなrpm
	python-imaging-devel-1.1.6-19.el6.x86_64
	python-imaging-1.1.6-19.el6.x86_64
	gnome-python2-bonobo-2.28.0-3.el6.x86_64
	gnome-python2-extras-2.25.3-20.el6.x86_64
	gnome-python2-applet-2.28.0-3.el6.x86_64
	gnome-python2-2.28.0-3.el6.x86_64

8.ライセンス
  GPLv3

9.使用ライブラリ
The Python Imaging Library is:
    Copyright © 1997-2005 by Secret Labs AB
    Copyright © 1995-2005 by Fredrik Lundh

10.変更履歴
2012.8.6	v0.4.0.0	0.4版リリース
						1画面のみの指定時は、各種設定ができずいきなり
						壁紙化する動作だったのを改善。
2012.7.9	v0.3.0.0	0.3版リリース無し
						python2.6下での開発に移行
						x86_64インストレーションに対応
2012.2.1	v0.2.0.0	初版(人柱版)リリース



