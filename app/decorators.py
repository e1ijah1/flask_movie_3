# -*- coding: utf-8 -*-
# Created by f1renze on 18-5-1 上午12:15
__author__ = 'f1renze'
__time__ = '18-5-1 上午12:15'

from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kw):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kw)
    return decorated_function
