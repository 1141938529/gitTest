from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Length


class PostForm(FlaskForm):
    content = TextAreaField('', render_kw={'placeholder': '这一刻的想法...'}, validators=[Length(5,200, message='说话要注意分寸，必须在5~200个字符之间！')])
    submit = SubmitField('发布')