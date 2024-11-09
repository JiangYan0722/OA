import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import User, EmailCaptcha
from exts import db

class RegisterForm(wtforms.Form):
    # 前端会传email
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误！')])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式有误！")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message='用户名格式有误！')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='密码太长或太短！')])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])

    # 自定义验证
    # 1. 邮箱是否已经被注册
    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册！")

    # 2. 验证码是否正确
    def validate_username(self, field):
        captcha = self.captcha.data
        email = self.email.data
        print("Debug: email =", email, "captcha =", captcha)  # 调试代码
        captcha_model = EmailCaptcha.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或验证码错误！")
        else:
            db.session.delete(captcha_model)
            db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误！')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='密码有误！')])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message="标题太长或太短！")])
    content = wtforms.StringField(validators=[Length(min=3, message="正文太少！")])


class AnswersForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=1, message="内容忒少！")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须要传入question_id")])