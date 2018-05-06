#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 13:53
__author__ = 'F1renze'
__time__ = '2018/3/18 13:53'

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

import hashlib

class VideoTag(db.Model):
    __tablename__ = 'video_tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    videos = db.relationship('Video', backref='video_tag',
                             lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return '<VideoTag %r>' % self.name

''' #使用多对多模型出现一系列问题??
# 1. (_mysql_exceptions.IntegrityError) (1215, 'Cannot add foreign key constraint')
# 2. 需要指定 foreign_keys
# 3. 需要指定 primaryjoin
# 4.sqlalchemy.exc.ArgumentError
#sqlalchemy.exc.ArgumentError: Could not locate any simple equality expressions involving locally mapped foreign key columns for primary join condition 'video_collect.user_id = "user".id' on relationship Video.collecters.  Ensure that referencing columns are associated with a ForeignKey or ForeignKeyConstraint, or are annotated in the join condition with the foreign() annotation. To allow comparison operators other than '==', the relationship can be marked as viewonly=True.

class VideoCollect(db.Model):
    __tablename__ = 'video_collect'
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<VideoCollect %r>' % self.id
'''
# 关联表
video_collect = db.Table('video_collect',
                         db.Column('video_id', db.Integer, db.ForeignKey('video.id')),
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                         )

video_like = db.Table('video_like',
                      db.Column('video_id', db.Integer, db.ForeignKey('video.id')),
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                      )

class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    intro = db.Column(db.Text)
    cover = db.Column(db.Unicode(255), unique=True)
    thumbnail_cover = db.Column(db.Unicode(255), unique=True)
    playnum = db.Column(db.BigInteger)
    tag_id = db.Column(db.Integer, db.ForeignKey('video_tag.id'))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    comments = db.relationship('Comment', backref='video',
                              lazy='dynamic', cascade='all, delete-orphan')
    # 收藏此视频的用户
    collecters = db.relationship('User', secondary=video_collect,
                 backref=db.backref('collect_videos', lazy='dynamic'),
                                 lazy='dynamic', single_parent=True)
    likers = db.relationship('User', secondary=video_like,
                             backref=db.backref('like_videos', lazy='dynamic'),
                             lazy='dynamic', single_parent=True)
    '''
    sqlalchemy.exc.ArgumentError
    sqlalchemy.exc.ArgumentError: On Video.collecters, delete-orphan cascade is not supported on a many-to-many or many-to-one relationship when single_parent is not set.   Set single_parent=True on the relationship().

    '''
    '''
    collecters = db.relationship('VideoCollect',
                                    foreign_keys=[VideoCollect.user_id],
                                    backref=db.backref('user', lazy='joined'),
                                    primaryjoin='VideoCollect.user_id==User.id',
                                    lazy='dynamic', cascade='all, delete-orphan')
    '''

    def __init__(self, **kwargs):
        super(Video, self).__init__(**kwargs)
        self.playnum = 0
        self.like = 0

    def play(self):
        self.playnum += 1
        db.session.add(self)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    def __repr__(self):
        return '<Video %r>' % self.title

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(11), index=True)
    location = db.Column(db.String(64))
    info = db.Column(db.Text)
    avatar_hash = db.Column(db.String(32))
    head_img = db.Column(db.Unicode(128), unique=False, nullable=True)
    thumb_head_img = db.Column(db.Unicode(128), unique=False, nullable=True)
    confirmed = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime(), default=datetime.now)
    last_visit = db.Column(db.DateTime(), default=datetime.now)
    get_like_num = db.Column(db.BigInteger)
    user_logs = db.relationship('UserLog', backref='user', lazy='dynamic',
                               cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic',
                               cascade='all, delete-orphan')
    # 用户收藏的视频
    '''
    collect_videos = db.relationship('VideoCollect', foreign_keys=[VideoCollect.video_id],
                                     backref=db.backref('user', lazy='joined'),
                                     primaryjoin='VideoCollect.video_id==Video.id',
                                     lazy='dynamic', cascade='all, delete-orphan')
    '''
    videos = db.relationship('Video', backref='uploader', lazy='dynamic',
                             cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if Admin.query.first() is None:
            admin = Admin(name='admin',
                          email=current_app.config['SITE_ADMIN_EMAIL'] or 'f1renze@163.com', password='admin')
            db.session.add(admin)
            try:
                db.session.commit()
            except:
                db.session.rollback()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

    def collect(self, video):
        if video not in self.collect_videos:
            # video_collect(video_id=video.id, user_id=self.id) # not callable
            self.collect_videos.append(video)
            db.session.add(self)
            try:
                db.session.commit()
                return True
            except:
                db.session.rollback()
                return False

    def uncollect(self, video):
        if video in self.collect_videos:
            self.collect_videos.remove(video)
            db.session.add(self)
            try:
                db.session.commit()
                return True
            except:
                db.session.rollback()
                return False

    def like(self, ip, video):
        if video not in self.like_videos:
            self.like_videos.append(video)
            user_log = UserLog(user=self, ip=ip, info='点赞['+video.title+']')
            db.session.add(user_log)
            db.session.add(self)
            try:
                db.session.commit()
                return True
            except:
                db.session.rollback()
                return False

    def unlike(self, ip, video):
        if video in self.like_videos:
            self.like_videos.remove(video)
            user_log = UserLog(user=self, ip=ip, info='取消点赞['+video.title+']')
            db.session.add(user_log)
            db.session.add(self)
            try:
                db.session.commit()
                return True
            except:
                db.session.rollback()
                return False

    def count_like_num(self):
        self.get_like_num = 0
        for video in self.videos:
            self.get_like_num += video.likers.count()
        db.session.add(self)
        try:
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @property
    def password(self):
        raise AttributeError('非明文密码, 不可读!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        try:
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        try:
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def ping(self):  # 刷新用户的最后访问时间
        self.last_visit = datetime.now()
        db.session.add(self)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    @property
    def is_admin(self):
        return False

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://cn.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size,
                                                                     default=default, rating=rating)

    def __repr__(self):
        return '<User %r>' % self.username


class UserLog(db.Model):
    __tablename__ = 'user_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(128), index=True)
    info = db.Column(db.String(32))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<UserLog %r>' % self.user.username

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    disabled = db.Column(db.Boolean)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Comment %r>' % self.content[:20]


class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128), nullable=False)
    admin_logs = db.relationship('AdminLog', backref='admin', lazy='dynamic')

    @property
    def is_admin(self):
        return True

    @property
    def password(self):
        raise AttributeError('密码不可读!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        admin = Admin.query.get(data.get('reset'))
        if admin is None:
            return False
        admin.password = new_password
        db.session.add(admin)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return True

    def __repr__(self):
        return '<Admin %r>' % self.name


class AdminLog(db.Model):
    __tablename__ = 'admin_log'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(128), index=True)
    info = db.Column(db.Text)
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<AdminLog %r>' % self.admin.email

