#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/21 9:06
__author__ = 'F1renze'
__time__ = '2018/3/21 9:06'

from . import auth
from flask import request, redirect, url_for, flash, render_template
from flask_login import current_user
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import login_user, login_required, logout_user, current_user
from app import db

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
    if current_user.is_authenticated and not current_user.confirmed \
        and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # flash('登录')
    alert_type='alert_info'
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remeber_me.data)
            return redirect(request.args.get('next') or url_for('home.index'))
        flash(u'无效用户名或密码')
    return render_template('auth/login.html', form=form, alert_type=alert_type)

@auth.route('/logout')
@login_required
def logout():
    login_user()
    flash('已经退出当前账户')
    return redirect(url_for('home.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/')

if __name__ == '__main__':
    pass