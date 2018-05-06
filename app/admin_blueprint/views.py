#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 13:54
__author__ = 'F1renze'
__time__ = '2018/3/18 13:54'

from app import db
from app.models import Video, User, VideoTag, UserLog, Comment, Admin, AdminLog
from app.admin_blueprint.modelviews import BaseModelView, \
    UserModelView, VideoModelView, CommentModelView, \
    AdminModelView, UserLogModelView, AdminLogModelView, TagModelView
from . import f_admin


f_admin.add_view(TagModelView(VideoTag, db.session, name='标签管理'))
f_admin.add_view(VideoModelView(Video, db.session, name='视频管理'))
f_admin.add_view(UserModelView(User, db.session, name='用户管理'))
f_admin.add_view(CommentModelView(Comment, db.session, name='评论管理', category='高级'))
f_admin.add_view(UserLogModelView(UserLog, db.session, name='用户日志', category='日志'))
#　需要指定 endpoint 创建单独的蓝本(admin蓝本已经被创建)
'''
AssertionError: A blueprint's name collision occurred between 
<flask.blueprints.Blueprint object at 0x7f6b875925f8> and 
<flask.blueprints.Blueprint object at 0x7f6b88879048>.  
Both share the same name "admin".  Blueprints that are created on the fly need unique names.
'''
f_admin.add_view(AdminModelView(Admin, db.session, name='管理员账户', endpoint='admin_account', category='高级'))
f_admin.add_view(AdminLogModelView(AdminLog, db.session, name='管理员日志', category='日志'))
