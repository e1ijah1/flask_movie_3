from threading import Thread
from flask import current_app, render_template
from flask_mail  import Message
from . import mail
from datetime import datetime

def send_async_email(app, msg):
    with app.app_context():
        # doc 中用法
        with mail.connect() as conn:
            conn.send(msg)
        # mail.send(msg) # py3报错:
        # smtplib.SMTPServerDisconnected: please run connect() first


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['SITE_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['SITE_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', dt=datetime.now(), **kwargs)
    msg.html = render_template(template + '.html', dt=datetime.now(), **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr