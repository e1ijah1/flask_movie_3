#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 15:47
__author__ = 'F1renze'
__time__ = '2018/3/18 15:47'

import os


class Config:
    # ADMIN_INDEX_URL = '/power'
    CACHE_DEFAULT_TIMEOUT = 50
    BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'
    SITE_NAME = 'CiliCili Video'
    VIDEO_COMMENTS_PER_PAGE = 5
    INDEX_VIDEO_PER_PAGE = 20
    SEARCH_PER_PAGE = 5

    SECRET_KEY = os.environ.get('SECRET_KEY') or '1A97885357271A95F8AFEDA2601B91B1'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True # 自动提交
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SITE_MAIL_SUBJECT_PREFIX = "[" + SITE_NAME + "] "
    SITE_MAIL_SENDER = os.environ.get('SITE_MAIL_SENDER')
    SITE_ADMIN_EMAIL = os.environ.get('SITE_ADMIN')
    SITE_DEFAULT_ADMIN_PASSWD = os.environ.get('SITE_DEFAULT_ADMIN_PASSWD')
    # flask-upload 设置
    UPLOADS_DEFAULT_DEST = os.path.join(os.path.abspath(os.path.dirname(__file__)), "app/static/uploads/")
    # 头像缩略图文件夹
    IMG_THUMB_DEST = os.path.join(os.path.abspath(os.path.dirname(__file__)), "app/static/uploads/thumbnails")

    # UPLOAD_URL = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")
    # VIDEO_UPLOAD_URL = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/videos/")
    # COVER_UPLOAD_URL = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/covers/")

    def __init__(self):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    HOSTNAME = os.environ.get('DB_HOST', '127.0.0.1')
    PORT = '3306'
    DATABASE = 'cili_db'
    DB_USERNAME = os.environ.get('DB_USERNAME', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{}:{}@localhost:{}/{}?charset=utf8'.format(
        DB_USERNAME, DB_PASSWORD, PORT, DATABASE
    )

    REDIS_URL = "redis://localhost:6379/1"

class ProductionConfig(Config):
    HOSTNAME = os.environ.get('DB_HOST')
    PORT = os.environ.get('DB_PORT')
    DATABASE = os.environ.get('DB_NAME')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(
        DB_USERNAME, DB_PASSWORD, HOSTNAME, PORT, DATABASE
    )

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}