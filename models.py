# 用于存放所创建的模型
from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now, nullable=False)

class EmailCaptcha(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    captcha = db.Column(db.String(60), nullable=False)
    used = db.Column(db.Boolean, nullable=False, default=False)


class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    # 外键
    auth_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship(User,backref=db.backref("questions"))


class Answer(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    # 外键
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # 关系
    question = db.relationship(Question, backref=db.backref("answers", order_by=create_time.desc())) # 反向引用，以后通过question可以拿到所有的
    author = db.relationship(User, backref="answers")