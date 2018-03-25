#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 13:54
__author__ = 'F1renze'
__time__ = '2018/3/18 13:54'

from . import home
from flask import render_template, flash

@home.route('/')
def index():
    flash(u'欢迎!')
    alert_type = 'alert-info'
    location = 'fixed-top'
    return render_template('home/index.html', alert_type=alert_type, location=location)
