#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 13:54
__author__ = 'F1renze'
__time__ = '2018/3/18 13:54'

from . import home
from flask import render_template, flash, current_app, redirect, url_for
from flask_login import login_required, current_user
from app.home.forms import VideoUpload
from werkzeug.utils import secure_filename
from app.models import Video
from app import db
import os, datetime, uuid


@home.route('/')
def index():
    flash(u'欢迎!')
    alert_type = 'alert-info'
    location = 'fixed-top'
    return render_template('home/index.html', alert_type=alert_type, location=location)

@home.route('/video/<int:id>', methods=['GET', 'POST'])
def video(id):
    return render_template('')

def expand_filename(filename):
    # 提取文件扩展名
    file_extend_name = os.path.splitext(filename)[-1]
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + file_extend_name
    return filename

@home.route('/video/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = VideoUpload()
    if form.validate_on_submit():
        video_filename = secure_filename(form.video.data.filename)
        cover_filename = secure_filename(form.cover.data.filename)
        if not os.path.exists(current_app.config['UPLOAD_URL']):
            os.makedir(current_app.config['UPLOAD_URL'])
            os.chmod(current_app.config['UPLOAD_URL'], 'rw')
            os.makedir(current_app.config['VIDEO_UPLOAD_URL'])
            os.chmod(current_app.config['VIDEO_UPLOAD_URL'], 'rw')
            os.makedir(current_app.config['COVER_UPLOAD_URL'])
            os.chmod(current_app.config['COVER_UPLOAD_URL'], 'rw')
        video_filename = expand_filename(video_filename)
        cover_filename = expand_filename(cover_filename)
        form.video.data.save(os.path.join(current_app.config['VIDEO_UPLOAD_URL'], video_filename))
        form.cover.data.save(os.path.join(current_app.config['COVER_UPLOAD_URL'], cover_filename))

        video = Video(
            title=form.data['title'],
            url=video_filename,
            intro=form.data['intro'],
            cover=cover_filename,
            upload_id=current_user.id
        )
        db.session.add(video)
        db.session.commit()
        flash('上传视频成功!')
        return redirect(url_for('home.video', id=video.id))
    return render_template('home/video/video_upload.html', form=form)