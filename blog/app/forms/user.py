from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, EqualTo, Email,ValidationError, DataRequired
from app.models import User
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.extensions import photos


# 定义用户注册表单类
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Length(4, 20, message='用户名必须在4~20个字符之间')])
    password = PasswordField('密码', validators=[Length(6, 20, message='密码长度必须在6~20个字符之间')])
    confirm = PasswordField('密码确认', validators=[EqualTo('password', message='密码必须一致')])
    email = StringField('邮箱', validators=[Email(message='请输入正确的邮箱格式')])
    submit = SubmitField('提交')

    # 自定义验证
    def validate_username(self, field):
        u = User.query.filter_by(username=field.data).first()
        if u:
            raise ValidationError('用户已存在！')

    # 邮箱校验
    def validate_email(self, field):
        u = User.query.filter_by(email=field.data).first()
        if u:
            raise ValidationError('邮箱已存在！')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember = BooleanField('记住我', default=False)
    submit = SubmitField('提交')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('原密码', validators=[DataRequired()])
    new_password = PasswordField('新密码', validators=[Length(6, 20, message='密码长度必须在6~20个字符之间')])
    confirm = PasswordField('密码确认', validators=[EqualTo('new_password', message='密码必须一致')])
    submit = SubmitField('确认修改')


class IconForm(FlaskForm):
    icon = FileField('个人头像', validators=[FileRequired(message='未上传头像'), FileAllowed(photos, message='请上传图片')])
    submit = SubmitField('上传')