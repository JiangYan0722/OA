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

#     class UserModel(db.Model):
#         __tablename__ = 'user_info'  # 假设表名为 user_info
#
#         user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#         user_name = db.Column(db.String(20), unique=True, nullable=False)
#         Tel = db.Column(db.String(11), unique=True, nullable=False)
#         birth_date = db.Column(db.Date, nullable=False)
#         gender = db.Column(db.Integer, comment='性别 1:男 2：女')
#
#         # 本科、硕士、博士（院校专业）
#         edu_level = db.Column(db.String(50), comment='学历 下拉框&单选')
#         school = db.Column(db.String(100), nullable=False, comment='院校 搜索框&单选——外置数据库')
#         major = db.Column(db.String(100), nullable=False, comment='专业 搜索框&单选——外置数据库')
#         class_year = db.Column(db.Integer, comment='年级')
#         major_level = db.Column(db.String(100), nullable=False, comment='专业水平 下拉框&单选')
#
#         advantage_subjects = db.Column(db.String(20), comment='优势学科大类 多选')
#         advantage_subjects_details = db.Column(db.String(100), comment='优势学科细类 自述')
#
#         personality_traits = db.Column(db.String(255), comment='个人性格/能力倾向 单选')
#         hobbies = db.Column(db.String(255), comment='兴趣爱好 文本框自述')
#         family_ecoStatus = db.Column(db.String(50), comment='家庭经济水平 单选')
#         origin = db.Column(db.String(100), comment='生源地 单选——外置数据库')
#         family_expectations = db.Column(db.String(255), comment='家庭期望/建议 文本框自述')
#
#     class CareerIntentionModel(db.Model):
#         __tablename__ = 'career_intention'  # 求职意向表
#
#         career_intention_id = db.Column(db.Integer, autoincrement=True, primary_key=True,comment='求职表id 主键')
#         user_id = db.Column(db.Integer, db.ForeignKey("user_info.user_id"), nullable=False)
#
#         desired_industry = db.Column(db.String(100), comment='意向行业 可复选&导航栏——外界数据库')
#         desired_position = db.Column(db.String(100), comment='意向职业 可复选&导航栏——外界数据库')
#         salary_expectation = db.Column(db.String(50), comment='薪资期望 单选')
#         work_location = db.Column(db.String(100), comment='工作地点 可复选——外界数据库')
#
#         # company_size = db.Column(db.String(50), comment='公司规模 可复选 \'小型\', \'中大型\', \'超大型\'')
#         # work_team_type = db.Column(db.String(50), comment='工作团体性质 可复选 \'机关单位\', \'私企\', \'国企\', \'外企\'')
#
#
# class UserCareerPlanningSituation(db.Model):
#     __tablename__ = 'user_career_planning_situation'  # 表名
#
#     planning_id = db.Column(db.Integer, unsigned=True, autoincrement=True, primary_key=True, comment='职业规划表id')
#     user_id = db.Column(db.Integer, db.ForeignKey("user_info.user_id"), nullable=False, comment='用户id')
#
#     job_difficulties = db.Column(db.Text, comment='具体困难 多选（其他自述）')
#
#     who_help = db.Column(db.String(255), comment='寻求帮助的人物角色 多选（其他自述）')
#     resource_from = db.Column(db.String(100), comment='获取信息的渠道 文本框自述')
#
#     needed_guidance = db.Column(db.Text, comment='需要哪些方面的指导或建议 文本框自述')
#     # is_demanding_skill_upgrading = db.Column(db.Integer, comment='有无技能提升需求 单选（有/无）')
#     # is_demanding_job_opportunity = db.Column(db.Integer, comment='是否需要提供就业机会 单选（是/否）')
#
#
# class Experience(db.Model):
#     __tablename__ = 'experience'  # 表名
#
#     experience_id = db.Column(db.Integer, unsigned=True, autoincrement=True, primary_key=True, comment='经历表id 主键')
#     user_id = db.Column(db.Integer, db.ForeignKey("user_info.user_id"))  # 确保用户ID不为空
#
#     # TODO:是否放到一个框里
#     project_experience = db.Column(db.Text, comment='项目经历 文本框自述')
#     internship_experience = db.Column(db.Text, comment='实习经历 文本框自述')
#     skill_certifications = db.Column(db.Text, comment='技能证书 文本框自述')
#
#     # 定义外键关系
#     user = db.relationship('User', backref=db.backref('experiences', lazy=True))
#
#
# class Conversation(db.Model):
#     __tablename__ = 'conversations'  # 表名
#
#     conversation_id = db.Column(db.Integer, unsigned=True, autoincrement=True, primary_key=True, comment='每轮对话id 主键')
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
#     agent_id = db.Column(db.Integer, unsigned=True, nullable=False, comment='关联智能体')
#     created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment='创建时间')
#     updated_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, comment='对话更新时间')
#
#     class Message(db.Model):
#         __tablename__ = 'messages'  # 表名
#
#         message_id = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='每次对话id 主键')
#         conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.conversation_id'), comment='关联每轮对话 外键')
#         user_message = db.Column(db.String(3000), nullable=False, comment='用户消息')
#         ai_message = db.Column(db.String(5000), nullable=False, comment='ai消息')