from flask import render_template, current_app
from flask_mail import Message
from threading import Thread

from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(
        current_app.config['MAIL_SUBJECT_PREFIX'] + subject,
        sender=current_app.config['MAIL_SENDER'],
        recipients=[to],
    )
    msg.html = render_template(f'mail/{template}.html', **kwargs)

    thr = Thread(target=send_async_email(current_app, msg))
    thr.start()

    return thr
