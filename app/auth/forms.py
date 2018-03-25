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
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64),
                                           Email()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField(u'记住我')
    login = SubmitField(u'登录')

class RegistrationForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64),
                                           Email()])
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 64),
                                               Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                                                      0, u'用户名只能以字母开头, '
                                                         u'且只能包含字母, 数字, '
                                                         u'点或下划线!')])
    password = PasswordField(u'密码', validators=[DataRequired(),
                                                EqualTo('password2',
                                                        message=u'两次密码必须一致')])
    password2 = PasswordField(u'确认密码', validators=[DataRequired()])
    register = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经被注册!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已经被使用!')


if __name__ == '__main__':
    pass