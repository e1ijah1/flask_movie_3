# -*- coding: utf-8 -*-
# Created by f1renze on 18-4-18 上午10:01
__author__ = 'f1renze'
__time__ = '18-4-18 上午10:01'

from flask import render_template, Markup
from . import home

@home.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 请求实体超出 web server 或者程序上传限制
@home.app_errorhandler(413)
def request_entity_too_large(e):
    return render_template('413.html'), 413