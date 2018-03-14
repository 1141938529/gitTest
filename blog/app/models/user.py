from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from flask import current_app, flash
from app.extensions import login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True)
    confirmed = db.Column(db.Boolean, default=False)

    # 添加头像属性
    icon = db.Column(db.String(64), default='default.jpg')

    # 关系
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    # 设置密码不能直接访问
    @property
    def password(self):
        raise AttributeError('密码不能直接访问')

    # 设置密码
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    # 校验密码
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成激活的token
    def generate_activate_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        return s.dumps({'uid': self.id})

    # 解密token
    @staticmethod
    def check_activate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except BadSignature:
            flash('非法的token')
            return False
        except SignatureExpired:
            flash('token已过期')
            return False

        u = User.query.get(data['uid'])
        if not u:
            flash('用户不存在')
            return False
        if u.confirmed:
            flash('用户已激活')
            return False
        u.confirmed = True
        db.session.add(u)
        return True


# 获取user的回调函数
@login_manager.user_loader
def user_loader(uid):
    return User.query.get(int(uid))


