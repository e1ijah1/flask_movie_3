#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 13:54
__author__ = 'F1renze'
__time__ = '2018/3/18 13:54'

from flask_admin import BaseView, expose
from flask import flash, redirect, render_template, request, url_for, abort, current_app
from app.admin_blueprint.forms import AdminLoginForm
from app import f_admin, db
from app.models import Video, User, VideoTag, UserLog, Comment, Admin, AdminLog
from app.admin_blueprint.modelviews import BaseModelView, \
    UserModelView, VideoModelView, CommentModelView, AdminModelView, UserLogModelView
from flask_login import login_user, logout_user, current_user, login_required
from app.decorators import admin_required


f_admin.add_view(BaseModelView(VideoTag, db.session, name='标签管理'))
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
f_admin.add_view(BaseModelView(AdminLog, db.session, name='管理员日志', category='日志'))



class MyView(BaseView):

    @expose('/')
    def index(self):
        return redirect('/admin')

    @expose('/login', methods=('GET', 'POST'))
    def admin_login(self):
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
                    return redirect(current_app.config['ADMIN_INDEX_URL'])
            flash('管理员账户认证失败!')
        return render_template('admin/login.html', form=form)

    @expose('/logout')
    @login_required
    def admin_logout(self):
        if not current_user.is_admin:
            abort(403)
        logout_user()
        flash('退出后台管理')
        return redirect(url_for('home.index'))


# endpoint 指定 url端点, 不需要加 /
f_admin.add_view(MyView(name='security', endpoint='sec'))