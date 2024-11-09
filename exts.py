# 避免“循环引用”而存放扩展、插件文件 （如flask-sqlalchemy)

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()