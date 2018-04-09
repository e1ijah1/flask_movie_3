#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 13:54
__author__ = 'F1renze'
__time__ = '2018/3/18 13:54'

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

images = UploadSet('images', IMAGES)

class VideoUpload(FlaskForm):
    title = StringField(label='视频标题', validators=[DataRequired('标题不能为空!'),
                                                  Length(1, 64)])
    video = FileField(label='文件', validators=[FileRequired('请上传视频文件!'),
                                              FileAllowed(['mp4', 'flv', 'avi', 'wmv', 'mov', 'webm', 'mpeg4', 'ts', 'mpg', 'rm', 'rmvb', 'mkv',], '不支持的视频格式!!')])
    intro = TextAreaField(label='简介', validators=[DataRequired('简介不能为空!')])
    cover = FileField(label='封面', validators=[FileRequired('请上传封面!'),
                                              FileAllowed(images, '不支持的图片格式!!')])
    submit = SubmitField('上传', render_kw={
        'class': 'btn btn-primary',
    })
