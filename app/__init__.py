#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 13:52
__author__ = 'F1renze'
__time__ = '2018/3/18 13:52'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_mail import Mail
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_moment import Moment
from flask_redis import FlaskRedis
from flask_admin import Admin
from flask_babelex import Babel

db = SQLAlchemy()
mail=Mail()
moment = Moment()
rd = FlaskRedis()
f_admin = Admin(name='后台管理', template_mode='bootstrap3', base_template='admin/mybase.html')
babel = Babel()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

videos = UploadSet('videos', ('mp4', 'flv', 'avi', 'wmv', 'mov', 'webm', 'mpeg4', 'ts', 'mpg', 'rm', 'rmvb', 'mkv'))
images = UploadSet('images', IMAGES)

def create_app(configname):
    app = Flask(__name__)
    app.config.from_object(config[configname])
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    rd.init_app(app)
    f_admin.index_view.url = app.config['ADMIN_INDEX_URL']
    f_admin.init_app(app)
    babel.init_app(app)

    # flask-upload
    configure_uploads(app, (videos, images))
    # 限制文件大小500MB
    '''声明　errorhandler 413 后, firefox显示连接已重置, 
    stack overflow　上说在生产环境中使用其他web server, 可以正常返回结果'''
    # patch_request_class(app, 2 * 1024 * 1024)

    from app.admin_blueprint import admin_blueprint
    app.register_blueprint(admin_blueprint)
    from app.home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

