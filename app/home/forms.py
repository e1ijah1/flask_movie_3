#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 13:54
__author__ = 'F1renze'
__time__ = '2018/3/18 13:54'

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp
from wtforms import ValidationError
from app import videos, images
from app.models import Video, User

class VideoUpload(FlaskForm):
    title = StringField(label='视频标题', validators=[DataRequired('标题不能为空!'),
                                                  Regexp("^(?!_)(?!.*?_$)[a-zA-Z0-9_\u4e00-\u9fa5]+$", 0,
                                                         '视频标题只能包含汉字, 数字, 字母及下划线, 并且不能以下划线开头和结尾！'),
                                                  Length(1, 64)])
    video = FileField(label='视频文件', validators=[FileRequired('请上传视频文件!'),
                                              FileAllowed(videos, '不支持的视频格式!!')
                                                ])
    intro = TextAreaField(label='简介', validators=[DataRequired('简介不能为空!')])
    cover = FileField(label='封面', validators=[FileRequired('请上传封面!'),
                                              FileAllowed(images, '不支持的图片格式!!')])
    submit = SubmitField('上传', render_kw={
        'class': 'btn btn-primary form-control',
    })

    def validate_title(self, field):
        if Video.query.filter_by(title=field.data).first():
            raise ValidationError('视频标题已经被使用啦！')

class CommentForm(FlaskForm):
    content = TextAreaField(label='内容', validators=[DataRequired('请输入评论内容!')])
    submit = SubmitField('发表评论', render_kw={
        "class": "btn btn-secondary"
    })

class SearchForm(FlaskForm):
    search = StringField(validators=[DataRequired('搜索内容为空！'), Length(1, 64)],
                          render_kw={
                              'class': 'form-control',
                              'placeholder': 'Search'
                          })
    submit = SubmitField('搜索', render_kw={
        'class': 'btn btn-success'
    })

class EditProfileForm(FlaskForm):
    username = StringField(label='用户名',
                           validators=[DataRequired('用户名不能为空!'),
                                       Regexp("^(?!_)(?!.*?_$)[a-zA-Z0-9_\u4e00-\u9fa5]+$", 0,
                                              '用户名只能包含汉字, 数字, 字母及下划线, 并且不能以下划线开头和结尾！'),
                                       Length(1, 128)],
                           render_kw={
                               'class': 'form-control'
                           })
    avatar = FileField(label='用户头像', validators=[FileAllowed(images, '不支持的图片格式!!')],
                       render_kw={
                           'class': 'form-control'
                       })
    location = StringField(label='所在地', validators=[Length(1, 64)],
                           render_kw={
                               'class': 'form-control'
                           })
    phone = StringField(label='手机号码', validators=[DataRequired('请填写手机号码'),
                                                  Length(1, 11),
                                                  Regexp("^(13[0-9]|14[579]|15[0-3,5-9]|17[0135678]|18[0-9])\d{8}$", 0,
                                                         '请填写正确的手机号码格式！')],
                        render_kw={
                            'class': 'form-control'
                        })
    intro = TextAreaField(label='个人简介')
    submit = SubmitField('完成编辑', render_kw={
        'class': 'btn btn-primary form-control'
    })

    def __init__(self, user, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经被使用！')
