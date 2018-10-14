FROM python:3.6-alpine

MAINTAINER f1renze <f1renze@126.com>

ENV WEB_CONFIG=production \
    DB_HOST=database \
    DB_PORT=3306 \
    DB_NAME=TEST \
    REDIS_HOST=redis \
    MAIL_SERVER=xx \
    SITE_MAIL_SENDER=xx \
    SITE_ADMIN=asd \
    SITE_DEFAULT_ADMIN_PASSWD=asd \