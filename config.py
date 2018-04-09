#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 15:47
__author__ = 'F1renze'
__time__ = '2018/3/18 15:47'

import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1A97885357271A95F8AFEDA2601B91B1'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SITE_MAIL_SUBJECT_PREFIX = "[CiliCili Video] "
    SITE_MAIL_SENDER = os.environ.get('SITE_MAIL_SENDER')
    SITE_ADMIN_EMAIL = os.environ.get('SITE_ADMIN')
    SITE_DEFAULT_ADMIN_PASSWD = os.environ.get('SITE_DEFAULT_ADMIN_PASSWD')
    UPLOAD_URL = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")
    VIDEO_UPLOAD_URL = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/videos/")
    COVER_UPLOAD_URL = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/covers/")

class DevelopmentConfig(Config):
    DEBUG = True
    PORT = '3306'
    DATABASE = 'my_movie'

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:toor@localhost:{}/{}?charset=utf8'.format(PORT, DATABASE)

class ProductionConfig(Config):
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = os.environ.get('DATABASE')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(DB_USERNAME, DB_PASSWORD, HOSTNAME,
                                                                                   PORT, DATABASE)

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}