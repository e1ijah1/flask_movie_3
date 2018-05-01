#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 13:53
__author__ = 'F1renze'
__time__ = '2018/3/18 13:53'

import os
from app import create_app, db
from app.models import User
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
    admin_index = app.config['ADMIN_INDEX_URL']
    return dict(search_form=search_form, site_name=site_name, admin_index=admin_index)



if __name__ == '__main__':
    manager.run()