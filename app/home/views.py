#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 13:54
__author__ = 'F1renze'
__time__ = '2018/3/18 13:54'

from . import home
from flask import render_template, flash, current_app, redirect, url_for, request, \
    abort
from flask_login import login_required, current_user
from app.home.forms import VideoUpload, CommentForm, SearchForm, EditProfileForm
from werkzeug.utils import secure_filename
from app.models import Video, Comment, User
from app import db
import os, uuid, stat
from datetime import datetime
from app import videos, images
from PIL import Image


@home.route('/')
def index():
    # flash('欢迎!')
    page = request.args.get('page', 1, type=int)
    pagination = Video.query.order_by(Video.add_time.desc()).paginate(page, per_page=current_app.config['INDEX_VIDEO_PER_PAGE'],
                                                                      error_out=False)
    videos = pagination.items
    return render_template('home/index.html', pagination=pagination, videos=videos)

@home.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    newest_comments = user.comments[-2:]
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (user.videos.count() - 1) // current_app.config['SEARCH_PER_PAGE'] + 1
    pagination = user.videos.paginate(page,
                                      per_page=current_app.config['SEARCH_PER_PAGE'],
                                      error_out=False)
    return render_template('home/user.html', user=user, comments=newest_comments, pagination=pagination)

@home.route('/user/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(user=current_user)
    if form.validate_on_submit():
        if not os.path.exists(current_app.config['UPLOADS_DEFAULT_DEST']):
            os.makedirs(current_app.config['UPLOADS_DEFAULT_DEST'])
            os.chmod(current_app.config['UPLOADS_DEFAULT_DEST'],
                     stat.S_IRWXU + stat.S_IRGRP + stat.S_IWGRP + stat.S_IROTH)
        elif not os.path.exists(current_app.config['IMG_THUMB_DEST']):
            os.makedirs(current_app.config['IMG_THUMB_DEST'])
            os.chmod(current_app.config['IMG_THUMB_DEST'],
                     stat.S_IRWXU + stat.S_IRGRP + stat.S_IWGRP + stat.S_IROTH)

        if form.avatar.data:
            avatar_filename = images.save(form.avatar.data)
            size = 50, 50
            im = Image.open(os.path.join(current_app.config['UPLOADS_DEFAULT_DEST'], 'images/', avatar_filename))
            im.thumbnail(size)
            file_split_name = os.path.splitext(avatar_filename)
            img_thumb = file_split_name[0] + '_thumbnail' + file_split_name[-1]
            im.save(os.path.join(current_app.config['IMG_THUMB_DEST'], img_thumb))
            current_user.thumb_head_img = url_for('static', filename='uploads/thumbnails/' + img_thumb)
            current_user.head_img = images.url(avatar_filename)

        if form.location.data:
            current_user.location = form.location.data
        if form.phone.data:
            current_user.phone = form.phone.data
        if form.intro.data:
            current_user.info = form.intro.data
        current_user.username = form.username.data

        db.session.add(current_user)
        try:
            db.session.commit()
            flash('个人资料已经更新！')
        except:
            flash('未知错误！请重试或联系管理员')
            db.session.rollback()

        return redirect(url_for('.user', username=current_user.username))
    form.username.data = current_user.username
    form.phone.data = current_user.phone
    form.intro.data = current_user.info
    form.location.data = current_user.location
    return render_template('home/edit_profile.html', form=form, user=current_user)

@home.route('/video/delete/<int:id>')
@login_required
def delete_video(id):
    video = Video.query.get_or_404(id)
    name = video.title
    if current_user != video.uploader:
        abort(403)
    db.session.delete(video)
    try:
        db.session.commit()
        flash('视频[ ' + name + ' ]已经删除')
    except:
        flash('未知错误！请重试或联系管理员')
        db.session.rollback()
    return redirect(url_for('.user', username=current_user.username))

@home.route('/comment/delete/<int:id>')
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    video_id = comment.video_id
    if current_user != comment.author:
        abort(403)
    db.session.delete(comment)
    try:
        db.session.commit()
        flash('评论删除成功')
    except:
        flash('未知错误！请重试或联系管理员')
        db.session.rollback()
    return redirect(url_for('.video', id=video_id))

#视频收藏
@home.route('/video/collect/<int:id>')
def video_collect(id):
    video = Video.query.get_or_404(id)
    if not current_user.is_authenticated:
        flash('你还没有登录呢, 请先登录!')
    else:
        if current_user.collect(video):
            # flash('视频收藏成功')
            return 'True'
        else:
            # flash('额, 发生未知错误, 请重试')
            return 'False'

@home.route('/video/uncollect/<int:id>')
def video_uncollect(id):
    video = Video.query.get_or_404(id)
    if not current_user.is_authenticated:
        flash('你还没有登录呢, 请先登录!')
    else:
        if current_user.uncollect(video):
            flash('视频已经从收藏中移除')
            return 'True'
        else:
            flash('额, 发生未知错误, 请重试')
            return 'False'

@home.route('/video/like/<int:id>')
def video_like(id):
    video = Video.query.get_or_404(id)
    if not current_user.is_authenticated:
        flash('你还没有登录呢, 请先登录!')
    else:
        current_user.like(video)

@home.route('/video/unlike/<int:id>')
def video_unlike(id):
    video = Video.query.get_or_404(id)
    if not current_user.is_authenticated:
        flash('你还没有登录呢, 请先登录!')



@home.route('/video/<int:id>', methods=['GET', 'POST'])
def video(id):
    video = Video.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, video=video, author=current_user)
        db.session.add(comment)
        try:
            db.session.commit()
            flash('成功发布评论')
        except:
            flash('未知错误！请重试或联系管理员')
            db.session.rollback()

        return redirect(url_for('.video', id=video.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (video.comments.count() -1) // current_app.config['VIDEO_COMMENTS_PER_PAGE'] + 1
    pagination = video.comments.order_by(Comment.add_time.asc()).paginate(page, per_page=current_app.config['VIDEO_COMMENTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    video.play()
    return render_template('home/video/video.html', video=video, form=form, comments=comments,
                           pagination=pagination)

def expand_filename(filename):
    # 提取文件扩展名
    file_extend_name = os.path.splitext(filename)[-1]
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + str('_') + str(uuid.uuid4().hex) + file_extend_name
    return filename

@home.route('/video/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = VideoUpload()
    if form.validate_on_submit():
        # 使用Flask-Uploads不需要使用此函数处理文件名
        # video_filename = secure_filename(form.video.data.filename)
        # cover_filename = secure_filename(form.cover.data.filename)
        if not os.path.exists(current_app.config['UPLOADS_DEFAULT_DEST']):
            os.makedirs(current_app.config['UPLOADS_DEFAULT_DEST'])
            os.chmod(current_app.config['UPLOADS_DEFAULT_DEST'],
                     stat.S_IRWXU + stat.S_IRGRP + stat.S_IWGRP + stat.S_IROTH)
            # os.makedir(current_app.config['VIDEO_UPLOAD_URL'])
            # os.chmod(current_app.config['VIDEO_UPLOAD_URL'], 'rw')
            # os.makedir(current_app.config['COVER_UPLOAD_URL'])
            # os.chmod(current_app.config['COVER_UPLOAD_URL'], 'rw')
        # 使用uploadset.save()
        video_filename = videos.save(form.video.data, name=expand_filename(form.video.data.filename))
        cover_filename = images.save(form.cover.data, name=expand_filename(form.cover.data.filename))
        # form.video.data.save(os.path.join(current_app.config['VIDEO_UPLOAD_URL'], video_filename))
        # form.cover.data.save(os.path.join(current_app.config['COVER_UPLOAD_URL'], cover_filename))

        video = Video(
            title=form.data['title'],
            url=video_filename,
            intro=form.data['intro'],
            cover=cover_filename,
            uploader=current_user
        )
        db.session.add(video)
        try:
            db.session.commit()
            flash('上传视频成功!')
        except:
            flash('未知错误！请重试或联系管理员')
            db.session.rollback()

        return redirect(url_for('home.video', id=video.id))
    return render_template('home/video/video_upload.html', form=form)


@home.route('/search', methods=['POST', 'GET'])
def search():
    form = SearchForm()
    key = request.args.get('key')
    if form.validate_on_submit():
        key = form.search.data
    elif key is None:
        flash('搜索内容不能为空！')
        return redirect(url_for('home.index'))
    query = Video.query.filter(Video.title.ilike('%' + key + '%'))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (query.count() -1) // current_app.config['SEARCH_PER_PAGE'] + 1
    pagination = query.order_by(Video.add_time.desc()).paginate(page,
                                                                per_page=current_app.config['SEARCH_PER_PAGE'],
                                                                error_out=False)
    pagination.key = key
    return render_template('home/search.html', pagination=pagination, key=key, query_count=query.count())
    # key = request.args.get('key', '')
    # if key == '':
    #     flash('搜索内容不能为空！')
    #     return redirect(url_for('home.index'))
    # query = Video.query.filter(Video.title.ilike('%' + key + '%'))


from app import rd
from flask import Response
import json
@home.route("/tm/", methods=['GET', 'POST'])
def tm():
    """
    弹幕消息处理
    """
    if request.method == "GET":
        # 获取弹幕消息队列
        id = request.args.get('id')
        # 存放在redis队列中的键值
        key = "video" + str(id)
        if rd.llen(key):
            msgs = rd.lrange(key, 0, 2999)
            res = {
                "code": 1,
                "danmaku": [json.loads(v) for v in msgs]
            }
        else:
            res = {
                "code": 1,
                "danmaku": []
            }
        resp = json.dumps(res)
    if request.method == "POST":
        # 添加弹幕
        data = json.loads(request.get_data())
        msg = {
            "__v": 0,
            "author": data["author"],
            "time": data["time"],
            "text": data["text"],
            "color": data["color"],
            "type": data['type'],
            "ip": request.remote_addr,
            "_id": datetime.datetime.now().strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex,
            "player": [
                data["player"]
            ]
        }
        res = {
            "code": 1,
            "data": msg
        }
        resp = json.dumps(res)
        # 将添加的弹幕推入redis的队列中
        rd.lpush("video" + str(data["player"]), json.dumps(msg))
    return Response(resp, mimetype='application/json')

# GET 404, POST 正常使用
def get_tm():
    if request.method == "GET":
        # 获取弹幕消息队列
        id = request.args.get('id')
        # 存放在redis队列中的键值
        key = "video" + str(id)
        if rd.llen(key):
            msgs = rd.lrange(key, 0, 2999)
            res = {
                "code": 1,
                "danmaku": [json.loads(v) for v in msgs]
            }
        else:
            res = {
                "code": 1,
                "danmaku": []
            }
        resp = json.dumps(res)
    return Response(resp, mimetype='application/json')

