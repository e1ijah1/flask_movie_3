FROM daocloud.io/nginx:1.13-alpine

MAINTAINER f1renze <f1renze@126.com>

ADD vhost.conf /etc/nginx/conf.d/default.conf

WORKDIR /var/www

CMD ["nginx", "-g", "daemon off;"]