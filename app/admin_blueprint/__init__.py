#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 13:52
__author__ = 'F1renze'
__time__ = '2018/3/18 13:52'

from flask import Blueprint

admin_blueprint = Blueprint('admin_blueprint', __name__)

from flask_admin import Admin
from .override_views import MyIndexView
f_admin = Admin(name='后台管理',
                template_mode='bootstrap3',
                base_template='admin/mybase.html',
                index_view=MyIndexView())

from  . import views, modelviews