# -*- coding: utf-8 -*-
# Created by f1renze on 18-4-23 下午10:07
__author__ = 'f1renze'
__time__ = '18-4-23 下午10:07'

from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, request

class BaseModelView(ModelView):

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))