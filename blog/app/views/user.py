from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from app.forms import RegisterForm, LoginForm, ChangePasswordForm, IconForm
from app.models import User
from app.extensions import db
from app.email import send_mail
from flask_login import login_user ,logout_user, login_required, current_user
from app.extensions import photos
import os
from PIL import Image

user = Blueprint('user', __name__)

@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        # 通过form的用户名判断用户存不存在。
        if not u:
            flash('用户名或密码有误')
            return render_template('user/login.html', form=form)
        if not u.confirmed:
            flash('用户未激活')
            return render_template('user/login.html', form=form)
        # 如果存在，再判断密码是否相等。
        if not u.verify_password(form.password.data):
            flash('用户名或密码有误')
            return render_template('user/login.html', form=form)
        # 登录，写入session。。。
        login_user(u, remember=form.remember.data)
        # 登录成功返回首页。
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('user/login.html', form=form)


@user.route('/logout/')
def logout():
    logout_user()
    flash('用户已退出')
    return redirect(url_for('main.index'))


@user.route('/test/')
@login_required
def test():
    return  '测试成功'

@user.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 根据form的数据，生成用户对象
        u = User(username=form.username.data, email=form.email.data,
                 password=form.password.data
                 )
        # 保存对象。
        db.session.add(u)
        # 增强代码强壮性，手动提交一次。
        db.session.commit()
        # 发送激活邮件。
        token = u.generate_activate_token()
        send_mail('用户激活', form.email.data, 'user/activate', username=form.username.data,
                  token=token)
        # 提示用户注册成功
        # 跳转
        flash('注册成功')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)


@user.route('/activate/<token>')
def activate(token):
    if User.check_activate_token(token):
        flash('激活成功')
        # 跳转首页
        return redirect(url_for('user.login'))
    else:
        flash('激活失败')
        return redirect(url_for('main.index'))


@user.route('/profile/')
def profile():
    return render_template('user/profile.html')


@user.route('/change_password/', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # 判断原密码是否正确
        if current_user.verify_password(form.old_password.data):

            # 保存新密码
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            # 给出提示，修改密码成功
            flash('密码修改成功，请重新登录')
            # 先退出
            logout_user()
            # 跳转到登录界面。
            return redirect(url_for('user.login'))
        else:
            flash('原密码输入不正确，请重新输入')

    return  render_template('user/change_password.html', form=form)


def random_string(length=32):
    import random
    base_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choice(base_str) for i in range(length))


@user.route('/icon/', methods=['GET', 'POST'])
def icon():
    form = IconForm()
    if form.validate_on_submit():
        # 获取上传的图片
        suffix = os.path.splitext(form.icon.data.filename)[1]
        # 生成随机文件名
        filename  = random_string() + suffix
        # 保存文件
        photos.save(form.icon.data, name=filename)
        # 生成缩略图
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
        img = Image.open(pathname)
        # 处理
        img.thumbnail((128,128))

        # 再保存
        img.save(pathname)
        # 之前老的图片要删除，除了默认图片
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.icon))

        # 把文件名存到数据库
        current_user.icon = filename
        db.session.add(current_user)
        flash('头像上传成功')
    img_url = photos.url(current_user.icon)
    return render_template('user/icon.html', form=form, img_url=img_url)