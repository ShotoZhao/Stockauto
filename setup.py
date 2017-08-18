#!/usr/bin/env python
# _*_ coding=utf-8 _*_

from distutils.core import setup

setup(name='stockauto',
      version='1.0',
      description='filter stock automaticlly',
      author='Shoto Zhao',
      author_email='micalun@gmail.com',
      url='https://github.com/ShotoZhao',
      packages=['stockauto'],
      package_dir={'': 'src'},
      requires=['pandas', 'numpy','pymongo'],
      )