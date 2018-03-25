#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 13:54
__author__ = 'F1renze'
__time__ = '2018/3/18 13:54'

from . import admin


@admin.route('/')
def index():
    return "<h1 style='color:red'>this is admin</h1>"