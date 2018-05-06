#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 13:54
__author__ = 'F1renze'
__time__ = '2018/3/18 13:54'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, \
    TextAreaField, FileField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from wtforms import ValidationError
from app.models import Video, VideoTag, User, Admin

class AdminLoginForm(FlaskForm):
    name = StringField('管理员账户', validators=[DataRequired('账户名不能为空!'), Length(1, 64),
                                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                   '用户名只能以字母开头, 且只能包含字母, 数字, 点或下划线!')])
    password = PasswordField('密码', validators=[DataRequired('密码不能为空!')])
    login = SubmitField('登录')

class GlobalSet(FlaskForm):
    admin_url = StringField(label='后台管理URL')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('现在的密码', validators=[DataRequired('密码不能为空')])
    password = PasswordField('新的密码', validators=[DataRequired('密码不能为空'),
                                                 EqualTo('password2', message='两个密码必须一致')])
    password2 = PasswordField('再次确认新的密码', validators=[DataRequired('密码不能为空')])
    submit = SubmitField('更改密码')

class PasswordResetRequestForm(FlaskForm):
    name = StringField('管理员账户名', validators=[DataRequired('账户名不能为空!'), Length(1, 64),
                                             Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                    '用户名只能以字母开头, 且只能包含字母, 数字, 点或下划线!')])
    email = StringField('邮箱', validators=[DataRequired('账户邮箱不能为空!'), Length(1, 64), Email()])
    submit = SubmitField('重置密码')

    def validate_email(self, field):
        if not Admin.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱不存在!')

    def validate_name(self, field):
        if not Admin.query.filter_by(name=field.data).first():
            raise ValidationError('管理员账户名不存在!')

class PasswordResetForm(FlaskForm):
    password = PasswordField('新密码', validators=[DataRequired('新密码不能为空!'),
                                                EqualTo('password2', message='两个密码必须一致!')])
    password2 = PasswordField('再次确认新密码', validators=[DataRequired('密码不能为空!')])
    submit = SubmitField('重置密码')

class ChangeEmailForm(FlaskForm):
    email = StringField('新邮箱', validators=[DataRequired('新邮箱不能为空地址!'), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired('密码不能为空!')])
    submit = SubmitField('更换新邮箱')

    def validate_email(self, field):
        if Admin.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被使用')

# 后台编辑表单
from flask_admin.form import BaseForm
from wtforms import TextAreaField
from wtforms.widgets import TextArea

class CKTextAreaWidget(TextArea):
    def __call__(self, field, *args, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] = 'ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, *args, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class UETextAreaWidget(TextArea):
    def __call__(self, field, *args, **kwargs):
        if kwargs.get('id'):
            kwargs['id'] = 'ue'
        else:
            kwargs.setdefault('id', 'ue')

        if kwargs.get('class'):
            kwargs['class'] = ''
        else:
            kwargs.setdefault('class', '')
        return super(UETextAreaWidget, self).__call__(field, *args, **kwargs)

class UETextAreaField(TextAreaField):
    widget = UETextAreaWidget()

class TagForm(BaseForm, FlaskForm):
    name = StringField('标签名', validators=[DataRequired('标签不能为空'), Length(1, 100),
                                          Regexp("^(?!_)(?!.*?_$)[a-zA-Z0-9_\u4e00-\u9fa5]+$", 0,
                                                 '标签只能包含汉字, 数字, 字母及下划线, 并且不能以下划线开头和结尾！')])

    def validate_name(self, field):
        if VideoTag.query.filter_by(name=field.data).first():
            raise ValidationError('标签名已经被使用了')

class VideoForm(BaseForm, FlaskForm):
    title = StringField('视频标题', validators=[DataRequired('视频标题不能为空'), Length(1, 200),
                                            Regexp("^(?!_)(?!.*?_$)[a-zA-Z0-9_\u4e00-\u9fa5]+$", 0,
                                                   '视频标题只能包含汉字, 数字, 字母及下划线, 并且不能以下划线开头和结尾！')])
    intro = CKTextAreaField('简介', validators=[DataRequired('简介不能为空')])

    def validate_title(self, field):
        if Video.query.filter_by(title=field.data).first():
            raise ValidationError('视频标题已经被使用了')

class UserForm(BaseForm, FlaskForm):
    username = StringField('用户名', validators=[DataRequired('用户名不能为空'),
                                              Regexp("^(?!_)(?!.*?_$)[a-zA-Z0-9_\u4e00-\u9fa5]+$", 0,
                                                     '用户名只能包含汉字, 数字, 字母及下划线, 并且不能以下划线开头和结尾！'),
                                              Length(1, 128)])
    phone = StringField('手机号码', validators=[DataRequired('请填写手机号码'),
                                            Length(1, 11),
                                            Regexp("^(13[0-9]|14[579]|15[0-3,5-9]|17[0135678]|18[0-9])\d{8}$", 0,
                                                   '请填写正确的手机号码格式！')])
    locaion = StringField('所在地', validators=[Length(1, 64)])
    info = UETextAreaField('用户简介')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经被使用了')

class AdminForm(BaseForm, FlaskForm):
    name = StringField('账户名', validators=[DataRequired('账户名不能为空！'), Length(1, 64),
                                          Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                 '用户名只能以字母开头, 且只能包含字母, 数字, 点或下划线!')])
    email = StringField('邮箱', validators=[DataRequired('邮箱不能为空！'), Length(1, 64), Email()])
    # confirmed = SelectField('确认邮箱', choices=[
    #     ('True', '是'), ('False', '否')
    # ])
    password = PasswordField('密码', validators=[DataRequired('密码不能为空！'),
                                               EqualTo('password2', message='两次密码必须一致')])
    password2 = PasswordField('再次确认密码', validators=[DataRequired('确认密码不能为空!')])

    def validate_email(self, field):
        if Admin.query.filter_by(email=field.data).first():
            raise ValidationError('此邮箱已经被使用')

    def validate_name(self, field):
        if Admin.query.filter_by(name=field.data).first():
            raise ValidationError('账户名已经被使用')


