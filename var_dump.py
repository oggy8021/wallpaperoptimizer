# -*- coding: utf-8 -*-
'''
PHP��var_dump�I�Ȃ���

Python/var_dump - PukiWiki
http://www.osarika.com/~coni/pukiwiki/index.php?Python%2Fvar_dump
'''
from pprint import pprint

def var_dump(obj):
  pprint(dump(obj))

def dump(obj):
  '''return a printable representation of an object for debugging'''
  newobj = obj
  if isinstance(obj, list):
    # ���X�g�̒��g��\���ł���`���ɂ���
    newobj = []
    for item in obj:
      newobj.append(dump(item))
  elif isinstance(obj, tuple):
    # �^�v���̒��g��\���ł���`���ɂ���
    temp = []
    for item in obj:
      temp.append(dump(item))
    newobj = tuple(temp)
  elif isinstance(obj, set):
    # �Z�b�g�̒��g��\���ł���`���ɂ���
    temp = []
    for item in obj:
      # item��class�̏ꍇ��dump()�͎�����Ԃ���,������set�Ŏg�p�ł��Ȃ��̂ŕ�����ɂ���
      temp.append(str(dump(item)))
    newobj = set(temp)
  elif isinstance(obj, dict):
    # �����̒��g�i�L�[�A�l�j��\���ł���`���ɂ���
    newobj = {}
    for key, value in obj.items():
      # key��class�̏ꍇ��dump()��dict��Ԃ���,dict�̓L�[�ɂȂ�Ȃ��̂ŕ�����ɂ���
      newobj[str(dump(key))] = dump(value)
  elif '__dict__' in dir(obj):
    # �V�����`���̃N���X class Hoge(object)�̃C���X�^���X��__dict__�������Ă���
    newobj=obj.__dict__
    if ' object at ' in str(obj) and not '__type__' in newobj:
      newobj['__type__']=str(obj).replace(" object at ", " #")
    for attr in newobj:
      newobj[attr]=dump(newobj[attr])
  return newobj
