FROM python:3.6-alpine

MAINTAINER f1renze <f1renze@126.com>

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk add --no-cache --virtual build-dependencies \
    gcc musl-dev \
    mysql-client mariadb-dev build-base \
    && pip install -r requirements.txt

WORKDIR /var/www