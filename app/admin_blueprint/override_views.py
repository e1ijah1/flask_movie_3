# -*- coding: utf-8 -*-
# Created by f1renze on 18-5-1 下午2:27
__author__ = 'f1renze'
__time__ = '18-5-1 下午2:27'

from flask_admin import AdminIndexView, expose
from flask_login import current_user, logout_user, login_user, login_required
from flask import redirect, request, flash, render_template, abort, url_for, current_app
from app.admin_blueprint.forms import AdminLoginForm, \
    ChangePasswordForm, ChangeEmailForm, PasswordResetRequestForm, PasswordResetForm
from app.models import AdminLog, Admin
from app.email import send_email
from app import db

class MyIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        return super(MyIndexView, self).index()

    @expose('/login ', methods=('GET', 'POST'))
    def login_view(self):
        form = AdminLoginForm()
        if form.validate_on_submit():
            admin = Admin.query.filter_by(name=form.name.data).first()
            if admin is not None and admin.verify_password(form.password.data):
                if current_user.is_authenticated:
                    logout_user()
                login_user(admin)
                flash('管理员登录成功!')
                # flash(request.endpoint)
                admin_log =  AdminLog(admin_id=admin.id,
                                      ip=request.remote_addr, info='登录后台')
                db.session.add(admin_log)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                finally:
                    return redirect(url_for('.index'))
            flash('管理员账户认证失败!')
        return render_template('admin/login.html', form=form)

    @expose('/logout')
    @login_required
    def logout_view(self):
        if not current_user.is_admin:
            abort(403)
        logout_user()
        flash('退出后台管理')
        return redirect(url_for('home.index'))

# endpoint 指定 url端点, 不需要加 /
# f_admin.add_view(MyView(name='security', endpoint='sec'))

    @expose('/email-confirm')
    @login_required
    def email_confirm_view(self):
        token = current_user.generate_confirmation_token()
        try:
            send_email(current_user.email, '确认管理员邮箱',
                       'admin/email/admin_confirm',
                       admin=current_user, token=token)
        except:
            return 'False'
        return 'True'


    @expose('/confirm/<token>')
    @login_required
    def confirm_view(self, token):
        if current_user.confirmed:
            return redirect(url_for('.index'))
        if current_user.confirm(token):
            flash('管理员邮箱确认成功')
        else:
            flash('确认链接过期或无效')
        return redirect(url_for('.index'))

    @expose('/confirm')
    @login_required
    def resend_confirmation(self):
        token = current_user.generate_confirmation_token()
        send_email(current_user.email, '确认管理员邮箱', 'auth/email/confirm', user=current_user, token=token)
        flash('一封新的确认邮件已经发送, 请检查你的邮箱')
        return redirect(url_for('.index'))

    @expose('/change_email', methods=('GET', 'POST'))
    @login_required
    def change_email_request(self):
        form = ChangeEmailForm()
        if form.validate_on_submit():
            if current_user.verify_password(form.password.data):
                new_email = form.email.data
                token = current_user.generate_email_token(new_email)
                send_email(new_email, '确认新邮箱地址', 'admin/email/change_email', admin=current_user, token=token)
                return redirect(url_for('.index'))
            else:
                flash('无效邮箱或密码')
        return render_template('admin/change_email.html', form=form)

    @expose('/change_email/<token>')
    @login_required
    def change_email_view(self, token):
        if current_user.change_email(token):
            flash('管理员' + current_user.name + ', 您的邮箱已经更改')
        else:
            flash('无效请求!')
        return redirect(url_for('.index'))

    @expose('/change-password', methods=('GET', 'POST'))
    @login_required
    def change_password_view(self):
        form = ChangePasswordForm()
        if form.validate_on_submit():
            if current_user.verify_password(form.old_password.data):
                current_user.password = form.password.data
                db.session.add(current_user)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                flash('管理员' + current_user.name + ', 您的密码已经更改')
                return redirect(url_for('.index'))
            else:
                flash('无效密码')
        return render_template('admin/change_password.html', form=form)

    @expose('/reset', methods=['GET', 'POST'])
    def password_reset_request(self):
        if not current_user.is_anonymous:
            return redirect(url_for('.index'))
        form = PasswordResetRequestForm()
        if form.validate_on_submit():
            admin = Admin.query.filter_by(email=form.email.data).first()
            if admin and admin.name == form.name.data:
                if admin.confirmed is not True:
                    flash('请求被拒绝: 管理员账户邮箱未确认!')
                    return redirect(url_for('.login_view'))
                token = admin.generate_reset_token()
                send_email(admin.email, '重置管理员账户密码', 'admin/email/reset_password',
                           admin = admin, token=token)
                flash('一封重置邮件已经发送, 请检查你的邮箱')
                return redirect(url_for('.login_view'))
            else:
                flash('账户邮箱与账户名不匹配!')
        return render_template('admin/reset_password_request.html', form=form)

    @expose('/reset/<token>', methods=('GET', 'POST'))
    def password_reset(self, token):
        if not current_user.is_anonymous:
            return redirect(url_for('.index'))
        form = PasswordResetForm()
        if form.validate_on_submit():
            if Admin.reset_password(token, form.password.data):
                flash('管理员账户密码已重置')
                return redirect(url_for('.login_view'))
            else:
                return redirect(url_for('.index'))
        return render_template('admin/reset_password.html', form=form)
