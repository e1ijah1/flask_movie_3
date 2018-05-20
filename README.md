# CiliCili Video
![Python Version](https://img.shields.io/badge/Python-3.6.3-blue.svg)
![Flask Version](https://img.shields.io/badge/Flask-0.12.2-green.svg)
![Author](https://img.shields.io/badge/Powered%20by-F1renze-blue.svg)

项目上线地址:  [http://www.cilivideo.top/](http://www.cilivideo.top/)(建议在 PC 上使用 火狐浏览器访问)

此项目是基于 Python / Flask 开发的小型视频网站, 使用 MySQL 作为存储数据库, Redis 提供缓存及弹幕队列支持, 使用开源的HTML5播放器 [DPlayer](https://github.com/MoePlayer/DPlayer) 作为播放器插件, 视频评论区使用了百度的 [UEditor](http://ueditor.baidu.com/website/) 作为编辑器, 视频上传界面使用 [ckeditor](https://ckeditor.com) 作为编辑器, 后台管理使用的是 [Flask-Admin](https://flask-admin.readthedocs.io/en/latest/).

## 主要功能
- [x] 注册/登录/登出, 重置密码, 更改邮箱, 更改密码
- [x] 一键初始化站点(添加管理员帐号, 添加视频分类)
- [x] 视频的上传, 删除, 评论/删除评论/屏蔽评论(管理员), 发送弹幕, 收藏及点赞, 支持搜索视频
- [x] 用户个人资料展示与编辑, 支持上传头像
- [x] 后台管理, 包括以下内容
	- 视频分类
	- 视频管理
	- 用户管理
	- 评论管理
	- 管理员账户
	- 用户日志(登录, 点赞, 删除视频)
	- 管理员日志(登录, 创建, 修改, 删除)
	- 静态文件管理

## 部署
可参考我的部署记录文章: [文章地址](http://www.f1renze.top/2018/05/17/Flask-Gunicorn-Nginx-%E9%83%A8%E7%BD%B2%E8%AE%B0%E5%BD%95/)
> 数据库: 需要在 MySQL 中创建字符集为 `utf8` 的名为 `cilicili` 的数据库
> 
> 配置: **需要在环境变量中配置以下变量**
```
$MAIL_SERVER 
$MAIL_USERNAME 
$MAIL_PASSWORD 
$SITE_ADMIN_MAIL 
$SITE_MAIL_SENDER 
$SITE_DEFAULT_ADMIN_PASSWD
```

## ToDo
- [ ] 制作 Docker 镜像
- [ ] 适应移动端
- [ ] 记录异常日志
- [ ] 后台监控服务器状态

## 截图
**首页**
![首页](./README_img/index.png)

**搜索**
![搜索](./README_img/search.png)

**用户资料**
![用户资料](./README_img/user_profile.png)

**资料编辑**
![资料编辑](./README_img/user_profile_edit.png)

**视频播放**
![视频播放](./README_img/video.png)

**点赞与弹幕**
![点赞](./README_img/like.png)

弹幕发送
![弹幕](./README_img/danmu.png)

**后台首页**
![后台首页](./README_img/admin_index.png)

**视频管理**
![视频管理](./README_img/admin_video.png)

**静态文件管理**
![静态文件管理](./README_img/admin_static.png)

**日志记录**
![日志记录](./README_img/admin_log.png)

**评论管理**
![评论管理1](./README_img/admin_comment2.png)

![评论管理2](./README_img/admin_comment.png)

## 反馈
有任何问题欢迎提 Issue, 共同进步!