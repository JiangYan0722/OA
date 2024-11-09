from flask import Flask, session, redirect, url_for, render_template, g
from flask_migrate import Migrate
import config # step2 将config文件与主入口文件产生关联
from exts import db, mail # step3 导入插件
from models import User
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp

app = Flask(__name__)

# 原来的配置
# app.config['SQLALCHEMY_DATABASE_URI'] =
# f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

# step2 产生关联后，绑定配置文件
# 有了配置文件后的配置：直接把模块加载进来，文件会自动读取配置信息
app.config.from_object(config)


# 这个方法可以先创建再绑定
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

# step4 注册蓝图，产生关联
app.register_blueprint(qa_bp, url_prefix='/qa')
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def hello_world():  # put application's code here
    return render_template('base.html')


@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)


# 上下文处理器
@app.context_processor
def my_context_processor():
    return {"user": g.user}

if __name__ == '__main__':
    app.run()
