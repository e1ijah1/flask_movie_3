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
from app.models import Video, Comment, User, UserLog, VideoTag, Admin
from app import db, cache
import os, uuid, stat
from datetime import datetime
from app import videos, images
from PIL import Image
from app.decorators import admin_required

@home.route('/initialize')
def initialize():
    admin_list = db.session.query(Admin).all()
    if admin_list:
        abort(404)
    flash('数据表创建成功!')
    admin = Admin(name='admin',
                  email='admin@admin.com', password='admin')
    db.session.add(admin)
    flash('管理员账户: admin 密码: admin 准备提交')
    tag_list = ['技术', '科普', '娱乐', '生活', '记录', '电影', '音乐']
    for t in tag_list:
        tag = VideoTag(name=t)
        db.session.add(tag)
        flash('标签列表准备提交')
    try:
        db.session.commit()
        flash('所有事务提交成功!')
    except:
        flash('未知错误!')
        db.session.rollback()
    return redirect(url_for('home.index'))

@home.route('/')
@cache.cached(30)
def index():
    # flash('欢迎!')
    page = request.args.get('page', 1, type=int)
    if Video.query.all() == None:
        pagination = None
        videos = None
    else:
        pagination = Video.query.order_by(Video.add_time.desc()).\
            paginate(page, per_page=current_app.config['INDEX_VIDEO_PER_PAGE'], error_out=False)
        videos = pagination.items
    tags = VideoTag.query.all()
    return render_template('home/index.html',
                           pagination=pagination, videos=videos, tags=tags)

@home.route('/tag/<tagname>')
@cache.cached()
def show_tag(tagname):
    page = request.args.get('page', 1, type=int)
    tag = VideoTag.query.filter_by(name=tagname).first()
    pagination = Video.query.filter_by(tag_id=tag.id).order_by(Video.add_time.desc())\
        .paginate(page, per_page=current_app.config['INDEX_VIDEO_PER_PAGE'], error_out=False)
    videos = pagination.items
    tags = VideoTag.query.all()
    return render_template('home/index.html', pagination=pagination,
                           videos=videos, tags=tags, active=tagname)

@home.route('/user/<username>')
@cache.cached()
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
    finally:
        return redirect(url_for('.video', id=video_id))

@home.route('/comment/disable/<int:id>')
@admin_required
def disable_comment(id):
    comment = Comment.query.get_or_404(id)
    video_id = comment.video_id
    comment.disabled = True
    db.session.add(comment)
    try:
        db.session.commit()
        flash('已经屏蔽此评论')
    except:
        flash('未知错误！')
        db.session.rollback()
    finally:
        return redirect(url_for('.video', id=video_id))

@home.route('/comment/enable/<int:id>')
@admin_required
def enable_comment(id):
    comment = Comment.query.get_or_404(id)
    video_id = comment.video_id
    comment.disabled = False
    db.session.add(comment)
    try:
        db.session.commit()
        flash('已经恢复此评论')
    except:
        flash('未知错误！')
        db.session.rollback()
    finally:
        return redirect(url_for('.video', id=video_id))

#视频收藏
@home.route('/video/collect/<int:id>')
def video_collect(id):
    video = Video.query.get_or_404(id)
    if current_user.collect(video):
        # flash('视频收藏成功')
        return 'True:'+str(video.collecters.count())
    else:
        # flash('额, 发生未知错误, 请重试')
        return 'False:'+str(video.collecters.count())

@home.route('/video/uncollect/<int:id>')
def video_uncollect(id):
    video = Video.query.get_or_404(id)
    if current_user.uncollect(video):
        # flash('视频已经从收藏中移除')
        return 'True:'+str(video.collecters.count())
    else:
        # flash('额, 发生未知错误, 请重试')
        return 'False:'+str(video.collecters.count())


@home.route('/video/like/<int:id>')
def video_like(id):
    video = Video.query.get_or_404(id)
    ip = request.remote_addr
    if current_user.like(ip, video):
        return 'True:'+str(video.likers.count())
    else:
        return 'False:'+str(video.likers.count())

@home.route('/video/unlike/<int:id>')
def video_unlike(id):
    video = Video.query.get_or_404(id)
    ip = request.remote_addr
    if current_user.unlike(ip, video):
        return 'True:'+str(video.likers.count())
    else:
        return 'False:'+str(video.likers.count())

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
        tag =  VideoTag.query.filter_by(name=form.data['tag']).first()
        if not tag:
            tag = VideoTag.query.first()
        video = Video(
            title=form.data['title'],
            url=video_filename,
            intro=form.data['intro'],
            cover=cover_filename,
            uploader=current_user,
            video_tag = tag
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

'''
弹幕处理工厂函数
'''
def danmu_factory(dict):
    l = []
    l.append(dict.get('time'))
    t = dict.get('type')
    if t == 'right':
        t = 0
    elif t == 'top':
        t = 1
    elif t == 'bottom':
        t = 2
    l.append(t)
    l.append(dict.get('color'))
    l.append(dict.get('author'))
    l.append(dict.get('text'))
    return l

'''
api url 升级为v2, 故变更为 '/<name>/v2/'
'''
from app import rd
from flask import Response
import json
@home.route("/danmu/v2/", methods=['GET', 'POST'])
# @cache.cached(30) 用缓存会发送不了弹幕
def danmu():
    if request.method == "GET":
        # 获取弹幕队列
        id = request.args.get('id')
        # 存放在redis队列中的键值
        key = "video:" + str(id)
        # Llen 获取列表长度
        if rd.llen(key):
            # Lrange 获取列表指定范围内的元素
            msgs = rd.lrange(key, 0, 2999)
            # msgs 是 bytes 的 list, json.loads(v) 得到 单条弹幕的 dict
            dict_list = [json.loads(v) for v in msgs]
            res = {
                "code": 0,
                "danmaku": [danmu_factory(d) for d in dict_list]
            }
        else:
            res = {
                "code": 0,
                "danmaku": []
            }

    elif request.method == "POST":
        # 添加弹幕, 将 JSON 转换回 Python 数据结构
        data = json.loads(request.get_data())
        msg = {
            "__v": 0,
            "author": data["author"],
            "time": data["time"],
            "text": data["text"],
            "color": data["color"],
            "type": data['type'],
            "ip": request.remote_addr,
            "referer": request.base_url,
            "_id": datetime.now().strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex,
            "player": [
                data["player"]
            ]
        }
        res = {
            "code": 0,
            "data": msg,
            "msg": '发送弹幕成功'
        }
        # 将添加的弹幕作为值转换为 JSON 推入redis的队列中
        # Lpush 将一个或多个值插入到列表头部
        rd.lpush("video:" + str(data["player"]), json.dumps(msg))

    resp = json.dumps(res)
    return Response(resp, mimetype='application/json')

