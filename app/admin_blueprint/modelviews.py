# -*- coding: utf-8 -*-
# Created by f1renze on 18-4-23 下午10:07
__author__ = 'f1renze'
__time__ = '18-4-23 下午10:07'

from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, current_app, flash
from flask_admin.model.template import macro
from jinja2 import Markup
from PIL import Image
from .forms import TagForm, VideoForm, UserForm, AdminForm
from app import db
from app.models import Admin, Video, User
import os

class BaseModelView(ModelView):

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login_view'))

    def is_accessible(self):
        return current_user.is_authenticated

class TagModelView(BaseModelView):
    # pass
    form = TagForm

    column_labels = {
        'name': '标签名',
        'add_time': '添加时间'
    }

class UserModelView(BaseModelView):
    can_create = False

    form = UserForm

    list_template = 'admin/list/_user_list.html'
    edit_template = 'admin/edit/_user_edit.html'

    def _list_thumb_head_img(view, context, model, name):
        if not model.thumb_head_img:
            return Markup('<img src="%s" alt="头像缩略图">' % model.gravatar(size=50))
        return Markup('<img src="%s" alt="头像缩略图">' % model.thumb_head_img)

    def _list_username(view, context, model, name):
        return Markup('<a href="%s" target="_blank">%s</a>' %
                      (url_for('home.user', username=model.username),
                       model.username))

    column_formatters = dict(info=macro('render_info'), head_img=macro('render_head_img'),
                             thumb_head_img=_list_thumb_head_img, phone=macro('render_phone'),
                             location=macro('render_location'),
                             get_like_num=macro('render_get_like_num'),
                             username=_list_username, confirmed=macro('render_confirmed'))

    column_labels = {
        'username': '用户名',
        'email': '邮箱',
        'phone': '手机号码',
        'location': '所在地',
        'info': '简介',
        'head_img': '头像',
        'thumb_head_img': '头像缩略图',
        'confirmed': '是否确认',
        'member_since': '注册时间',
        'last_visit': '最后访问',
        'get_like_num': '获得赞数'
    }

    column_exclude_list = ['password_hash', 'avatar_hash']

class VideoModelView(BaseModelView):
    form = VideoForm

    edit_template = 'admin/edit/_video_edit.html'

    # form_overrides = {
    #     'intro': CKTextAreaField
    # }

    can_create = False

    list_template = 'admin/list/_video_list.html'

    def _list_thumbnail_cover(view, context, model, name):
        # 设置缩略图
        size = 200, 200
        im = Image.open(os.path.join(current_app.config['UPLOADS_DEFAULT_DEST'], 'images/', model.cover))
        im.thumbnail(size)
        extension = os.path.splitext(model.cover)
        thumbnail_name = extension[0] + '_thumbnail' + extension[-1]
        im.save(os.path.join(current_app.config['IMG_THUMB_DEST'], thumbnail_name))
        model.thumbnail_cover = url_for('static', filename='uploads/thumbnails/' + thumbnail_name)
        return Markup('<img src="%s" alt="视频封面"' % model.thumbnail_cover)

    def _list_url(view, context, model, name):
        return Markup('<a href="%s" target="_blank">视频链接</a>' % url_for('home.video', id=model.id))

    def _list_uploader(view, context, model, name):
        return Markup('<a href="%s" target="_blank">%s</a>' % (url_for('home.user', username=model.uploader.username),
                                                               model.uploader.username))

    column_formatters = dict(intro=macro('render_intro'),
                             thumbnail_cover=_list_thumbnail_cover,
                             url=_list_url, video_tag=macro('render_video_tag'),
                             uploader=_list_uploader)

    column_exclude_list = ['cover',]

    column_labels = {
        'title': '视频标题',
        'intro': '视频简介',
        'thumbnail_cover': '封面缩略图',
        'playnum': '播放数',
        'add_time': '上传时间',
        'video_tag': '视频标签',
        'uploader': '上传者'
    }

class CommentModelView(BaseModelView):
    can_create = False
    can_edit = False

    list_template = 'admin/list/_comment_list.html'

    def _list_video(view, context, model, name):
        return Markup('<a href="%s" target="_blank">%s</a>' % (url_for('home.video', id=model.video.id),
                                                               model.video.title))

    def _list_author(view, context, model, name):
        return Markup('<a href="%s" target="_blank">%s</a>' % (url_for('home.user', username=model.author.username),
                                                               model.author.username))

    column_formatters = dict(content=macro('render_content'), video=_list_video, author=_list_author)

    column_labels = {
        'content': '评论内容',
        'video': '评论于',
        'author': '评论者',
        'add_time': '评论时间',
        'disabled': '屏蔽评论'
    }

    column_list = ('content', 'author', 'video', 'add_time', 'disabled')

class AdminModelView(BaseModelView):
    can_edit = False

    form = AdminForm

    def on_model_change(self, form, model, is_created):
        if is_created and form.validate_on_submit():
            admin = Admin(name=form.name.data,
                          email=form.email.data,
                          password=form.password.data)
            db.session.add(admin)
            try:
                db.session.commit()
            except:
                db.session.rollback()

    column_exclude_list = ['password_hash']

    column_labels = {
        'name': '账户名',
        'email': '账户邮箱',
        'confirmed': '确认邮箱'
    }

    list_template = 'admin/list/_admin_list.html'

    column_formatters = dict(confirmed=macro('render_confirmed'))

class UserLogModelView(BaseModelView):
    can_create = False
    can_edit = False

    column_list = ('info', 'user', 'ip', 'add_time')

    column_labels = {
        'info': '日志摘要',
        'user': '用户',
        'ip': 'IP地址',
        'add_time': '时间'
    }

    def _list_user(view, context, model, name):
        return Markup('<a href="%s" target="_blank">%s</a>' % (url_for('home.user', username=model.user.username),
                                                               model.user.username))

    column_formatters = dict(user=_list_user)

class AdminLogModelView(BaseModelView):
    can_create = False
    can_edit = False
    can_delete = False

    column_list = ('info', 'admin', 'ip', 'add_time')

    column_labels = {
        'info': '日志摘要',
        'admin': '管理员',
        'ip': 'IP地址',
        'add_time': '时间'
    }

    def _list_admin(view, context, model, name):
        return Markup('<b>%s</b>' % model.admin.name)

    column_formatters = dict(admin=_list_admin)