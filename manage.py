#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 13:53
__author__ = 'F1renze'
__time__ = '2018/3/18 13:53'

import os
from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('WEB_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command('shell', Shell())
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()