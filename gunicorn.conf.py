# -*- coding: utf-8 -*-
# Created by f1renze on 18-5-15 上午10:35
__author__ = 'f1renze'
__time__ = '18-5-15 上午10:35'

# 定义同时开启的处理请求的进程数量, workers = multiprocessing.cpu_count() * 2 + 1
workers = 3
# 采用gevent库, 支持异步处理请求, 提高吞吐量
worker_class = 'gevent'
# 监听IP放宽, 以便于Docker之间/Docker和宿主机之间的通信
bind = '0.0.0.0:8000'

# 后台
daemon = True
loglevel = 'warning'
# 访问日志文件
accesslog = './logs/gunicorn_access.log'
# 错误日志文件
errorlog = './logs/gunicorn_error.log'