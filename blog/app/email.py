from .extensions import mail
from flask import current_app, render_template
from flask_mail import Message
from threading import Thread


def async_send_mail(app, msg):
    # 发邮件需要app的上下文，所以创建一个上下文对象。
    with app.app_context():
        mail.send(msg)



# 封装发送邮件的函数
def send_mail(subject, to, template, **kwargs):
    # 通过current_app代理对象，获取app实例对象
    app = current_app._get_current_object()

    msg = Message(subject=subject, recipients=[to,], sender=app.config['MAIL_USERNAME'])

    msg.html = render_template(template + '.html', **kwargs)
    msg.body = render_template(template + '.txt', **kwargs)

    # 新建一个线程
    thr = Thread(target=async_send_mail, args=[app, msg])
    #mail.send(msg)
    thr.start()
    return thr
