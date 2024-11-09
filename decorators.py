# 装饰器
from functools import wraps # 保留原来函数信息
from flask import g, redirect, url_for, session, flash, request, abort

def login_required(func):
    # 保留func的信息
    @wraps(func)
    def inner(*args, **kwargs):# 万能参数
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    return inner

# @login_required()
# def public_question():
#     pass
# login_required(public_question)(question_id)