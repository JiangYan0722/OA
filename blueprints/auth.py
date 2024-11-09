from flask import Blueprint,render_template, jsonify, redirect, url_for, session# 要渲染模板
from exts import mail, db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptcha
from .forms import RegisterForm, LoginForm
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
# 创建（蓝图名字，固定搭配，url前缀）
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else: # 其实就是提交请求
        form = LoginForm(request.form)
        if form.validate():
            # 存储数据
            user_email = form.email.data
            user_password = form.password.data # 我们通过加密方式存储的密码不能直接被使用
            user = User.query.filter_by(email=user_email).first()
            # 从数据库中查找
            if not user:
                print("邮箱不存在！")
                return redirect(url_for('auth.login'))
            if check_password_hash(user.password, user_password):
                # 账号密码都正确，使其处于一种登陆状态
                # cookie:(用于识别你是谁——存储少量数据用于登录授权)
                # session: flask中的session是通过加密存储在cookie中
                session['user_id'] = user.id
                return redirect('/')
            else:
                print("密码错误！")
                return redirect(url_for('auth.login'))

        else:
            print(form.errors)
            return redirect(url_for('auth.login'))


# GET：从服务器上获取数据
# POST：将客户端数据提交给服务器
@bp.route('/register', methods=['GET', 'POST']) # 指定只能是GET/POST请求，其他请求会出现405ERROR
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 如何验证用户输入的验证码和实际验证码一样？——自己在服务器上也存储一份captcha
        # 表单验证：flask-wtf
        # 现在要去获取注册页面的input标签中的内容
        form = RegisterForm(request.form)
        if form.validate():
            # 存储数据
            usr_email = form.email.data
            user_username = form.username.data
            user_password = form.password.data
            user = User(email= usr_email, username=user_username, password=generate_password_hash(user_password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.register'))


@bp.route('/logout')
def logout():
    # 退出登陆的逻辑就是删除session
    session.clear()
    return redirect("/")

@bp.route('/captcha/email')
def get_email_captcha():
    # 获取用户输入的邮箱
    # 传参的方式
    # /captcha/email/<email>
    # /captcha/email?email=xxx@xxx
    email = request.args.get('email')
    source = string.digits*4
    # 定义验证码
    captcha = random.sample(source,4)
    # print(captcha) #['5', '9', '3', '4']这还只是列表
    captcha = ''.join(captcha) # 拼接字符串
    message = Message(subject="您的验证码，请接收！", recipients=[email], body=f"您的验证码是：{captcha}，请不要告诉别人哦^_^")
    mail.send(message)
    # redis/memcached（网站数据多）
    # 数据库存储（网站数据少）
    email_captcha = EmailCaptcha(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit() # 提交到数据库
    # 返回数据要满足RESTful API
    # {code: 200/400/...; message: "", data: {}}
    return jsonify({"code": 200, "message": "", "data": None})


@bp.route('/mail/test')
def mail_test():
    # 主题、收件人、body
    message = Message(subject="flask邮箱连接测试", recipients=['1917811712@qq.com'], body="这是一封测试邮件——flask!")
    mail.send(message)
    return "邮件发送成功！"