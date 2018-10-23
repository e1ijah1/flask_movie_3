#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 13:53
__author__ = 'F1renze'
__time__ = '2018/3/18 13:53'

import os
from app import create_app, db
from app.models import Admin, VideoTag
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.home.forms import SearchForm

app = create_app(os.getenv('WEB_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
db_engine  = db.get_engine(app)

def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@app.context_processor
def inject_param():
    search_form = SearchForm()
    site_name = app.config['SITE_NAME']
    # admin_index = app.config['ADMIN_INDEX_URL']
    return dict(search_form=search_form, site_name=site_name)


@manager.command
def initialize():
    # print(app.config)
    if not database_is_empty():
        print('Pls don\'t repeat initialization!')
        return
    db.create_all()
    print('create tables success!')
    admin = Admin(
        name=app.config['DEFAULT_ADMIN'],
        email=app.config['DEFAULT_ADMIN_EMAIL'],
        pwd=app.config['DEFAULT_ADMIN_PWD']
    )
    db.session.add(admin)
    tag_list = ['技术', '科普', '娱乐', '生活', '记录', '电影', '音乐']
    for t in tag_list:
        tag = VideoTag(name=t)
        db.session.add(tag)
    try:
        db.session.commit()
        print(f'初始化成功!管理员账户: {admin.name}, 密码: {app.config["DEFAULT_ADMIN_EMAIL"]}')
    except Exception as e:
        print('初始化失败')
        print(e)
        db.session.rollback()


def table_exists(name):
    result = db_engine.dialect.has_table(db_engine, name)
    print(f'Table {name} exists: {result}')
    return result


def database_is_empty():
    table_names = db.inspect(db_engine).get_table_names()
    result = table_names == []
    print(f'DB is empty: {result}')
    return result


if __name__ == '__main__':
    manager.run()
