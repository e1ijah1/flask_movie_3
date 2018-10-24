# -*- coding: utf-8 -*-

# import sendgrid
from . import mail
# from sendgrid.helpers.mail import Email, Content
from threading import Thread
from datetime import datetime
from flask_mail import Message
from flask import current_app, render_template


def send_async_email(app, msg):
    with app.app_context():
        # doc 中用法
        with mail.connect() as conn:
            conn.send(msg)
        # mail.send(msg) # py3报错:
        # smtplib.SMTPServerDisconnected: please run connect() first


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', dt=datetime.now(), **kwargs)
    msg.html = render_template(template + '.html', dt=datetime.now(), **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

# def send_email(to, subject, template, **kws):
#     sg = sendgrid.SendGridAPIClient(apikey=current_app.config['MAIL_PASSWORD'])
#     from_email = Email(current_app.config['MAIL_SENDER'])
#     to_email = Email(to)
#     # MIME type
#     content = Content('text/plain')
