#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 13:52
__author__ = 'F1renze'
__time__ = '2018/3/18 13:52'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(configname):
    app = Flask(__name__)
    app.config.from_object(config[configname])
    db.init_app(app)
    login_manager.init_app(app)

    from app.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/manage')
    from app.home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

