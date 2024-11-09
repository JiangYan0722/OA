# 配置文件 step1

SECRET_KEY = 'apple'

# 数据库配置
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "123456"
DATABASE = "zhiliaooa"
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI


# 邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_PORT = 587
MAIL_USERNAME = '1917811712@qq.com'
MAIL_PASSWORD = 'zmhrsqifittmbiid'
MAIL_DEFAULT_SENDER = '1917811712@qq.com'