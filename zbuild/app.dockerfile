FROM python:3.6-alpine

MAINTAINER f1renze <f1renze@126.com>

WORKDIR /var/www

ADD requirements.txt /var/www/

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk add --no-cache --virtual build-dependencies \
    # gevent
    gcc musl-dev \
    # mysqlclient
    mariadb-dev build-base \
    # pillow
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    # mysql cli
    mysql-client \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
