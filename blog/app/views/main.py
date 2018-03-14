from flask import Blueprint, render_template, current_app, flash, redirect, url_for, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.forms import PostForm
from app.models import Post
from flask_login import current_user
from app.extensions import db

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        # 保存用户的输入。
        # 获取对象，通过current_user对象来获取
        u = current_user._get_current_object()
        # 判断用户是否登录
        if u.is_authenticated:
            post = Post(content=form.content.data, user=u)
            # 保存对象
            db.session.add(post)
            form.content.data = ''
            flash('发布成功')
        else:
            flash('请登录再发布')
            return redirect(url_for('user.login'))
    #posts = Post.query.filter_by(rid=0).order_by(Post.timestamp.desc()).all()
    page = int(request.args.get('page', 1))
    pagination = Post.query.filter_by(rid=0).order_by(Post.timestamp.desc()).paginate(
        page=page,per_page=3, error_out=False)
    posts = pagination.items
    return render_template('main/index.html', form=form, posts=posts, pagination=pagination)


@main.route('/generate/')
def generate():
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
    data = s.dumps({'id': 250})
    return data


@main.route('/check/')
def check():
    s = Serializer(current_app.config['SECRET_KEY'])
    data = s.loads('eyJhbGciOiJIUzI1NiIsImlhdCI6MTUxMzY2NDgzNywiZXhwIjoxNTEzNjY4NDM3fQ.eyJpZCI6MjUwfQ.DKBFnaKrr9rJoE8mISOtavkisjXdmbfARXqDWaSA5L8')
    return str(data['id'])