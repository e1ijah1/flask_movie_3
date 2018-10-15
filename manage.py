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
    db.create_all()
    print('create tables success!')
    from app.models import Admin
    admin = Admin(name='admin', email='admin@admin.com', password='admin')
    db.session.add(admin)
    tag_list = ['技术', '科普', '娱乐', '生活', '记录', '电影', '音乐']
    for t in tag_list:
        tag = VideoTag(name=t)
        db.session.add(tag)
    try:
        db.session.commit()
        print(f'初始化成功!管理员账户: {admin.name}, 密码: admin')
    except Exception as e:
        print('初始化失败')
        print(e)
        db.session.rollback()


if __name__ == '__main__':
    manager.run()