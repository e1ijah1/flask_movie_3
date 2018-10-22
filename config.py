#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 15:47
__author__ = 'F1renze'
__time__ = '2018/3/18 15:47'

import os


class Config:
    SITE_NAME = 'CiliCili Video'
    SECRET_KEY = os.environ.get('SECRET_KEY', '1A97885357271A95F8AFEDA2601B91B1')

    # initial setting
    DEFAULT_ADMIN = os.environ.get('ADMIN', 'admin')
    DEFAULT_ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@admin.com')
    DEFAULT_ADMIN_PWD = os.environ.get('ADMIN_PWD', 'admin')

    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT', 465)
    MAIL_USE_SSL = True
    # mail login
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = "[" + SITE_NAME + "] "
    MAIL_SENDER = os.environ.get('MAIL_SENDER')

    # Redis
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
    REDIS_DB = os.environ.get('REDIS_DB', 1)
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

    # MySQL
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', 3306)
    MYSQL_DB = os.environ.get('MYSQL_DB', 'cili_db')
    MYSQL_USR = os.environ.get('MYSQL_USR', 'root')
    MYSQL_PWD = os.environ.get('MYSQL_PWD', '')
    SQLALCHEMY_DATABASE_URI = f'mysql://{MYSQL_USR}:{MYSQL_PWD}' \
                              f'@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8'

    # ADMIN_INDEX_URL = '/power'  # admin login page url
    # flask-caching timeout
    CACHE_DEFAULT_TIMEOUT = 50
    BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'

    # comment nums per page in video detail
    VIDEO_COMMENTS_PER_PAGE = 5
    # video nums in index
    INDEX_VIDEO_PER_PAGE = 20
    # result nums in search page
    SEARCH_PER_PAGE = 5

    # sqlalchemy
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 自动提交
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
