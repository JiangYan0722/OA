from flask import Blueprint, render_template, request, g, redirect, url_for
from .forms import QuestionForm,AnswersForm
from models import Question, Answer
from exts import db
from decorators import login_required

bp = Blueprint('qa', __name__, url_prefix='/')


# http://127.0.0.1:5000
@bp.route('/')
def index():
    # 显示所有问答
    questions = Question.query.order_by(Question.create_time.desc()).all()
    return render_template('index.html', questions=questions)

@bp.route('/public', methods=['GET', 'POST'])
@login_required
def public_question():
    if request.method == 'GET':
        return render_template('public_question.html')
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = Question(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect("/qa")
        else:
            print(form.errors)
            return redirect('/auth/login')


@bp.route("/detail/<qa_id>")
def qa_detail(qa_id):
    question = Question.query.get(qa_id)
    return render_template("detail.html",question=question)



@bp.post("/answer/public")# @bp.route('/answer/public', methods=['POST'])
@login_required
def public_answer():
    form = AnswersForm(request.form)
    # 验证表单是否正确
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = Answer(content=content, question_id=question_id, reviewer_id = g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('qa.qa_detail', qa_id=question_id))
    # 验证失败做什么
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))


@bp.route("/search")
@login_required
def search():
    # 查询内容的3种方式
    # /search?q=flask
    q = request.args.get("q")
    questions = Question.query.filter(Question.title.contains(q)).all()
    return render_template("index.html", questions=questions)
    # /search/<q>
    # post,request.form