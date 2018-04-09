#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/21 9:06
__author__ = 'F1renze'
__time__ = '2018/3/21 9:06'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import  DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                           Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    login = SubmitField('登录')

class RegistrationForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                           Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64),
                                               Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                                                      0, '用户名只能以字母开头, '
                                                         '且只能包含字母, 数字, '
                                                         '点或下划线!')])
    password = PasswordField('密码', validators=[DataRequired(),
                                                EqualTo('password2',
                                                        message='两次密码必须一致')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    register = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经被使用!')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('现在的密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[DataRequired(),
                                                EqualTo('password2', message='两个密码必须一致!')])
    password2 = PasswordField('再次确认新密码', validators=[DataRequired()])
    submit = SubmitField('修改密码')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('重置密码')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱不存在!')

class PasswordResetForm(FlaskForm):
    password = PasswordField('新密码', validators=[DataRequired(),
                                                EqualTo('password2', message='两个密码必须一致!')])
    password2 = PasswordField('再次确认新密码', validators=[DataRequired()])
    submit = SubmitField('重置密码')

class ChangeEmailForm(FlaskForm):
    email = StringField('新邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('更换邮箱')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册!')

if __name__ == '__main__':
    pass