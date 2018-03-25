#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/21 8:54
__author__ = 'F1renze'
__time__ = '2018/3/21 8:54'

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views

if __name__ == '__main__':
    pass