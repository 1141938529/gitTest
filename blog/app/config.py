import os

base_dir = os.path.abspath(os.path.dirname(__file__))


# 通用配置
class Config:
    # 秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'
    # 数据库
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 邮件发送
    MAIL_SERVER  = os.environ.get('MAIL_SERVER') or 'smtp.1000phone.com'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'xuke@1000phone.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'X!uke123'

    # 文件上传的配置
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'static/upload')
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024

    # 额外的初始化操作
    @staticmethod
    def init_app(self):
        pass


# 开发环境
class DevelopmentConfig(Config):
    # 数据库连接
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-dev.sqlite')


# 测试环境
class TestingConfig(Config):
    # 数据库连接
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-test.sqlite')


# 生产环境
class ProductionConfig(Config):
    # 数据库连接
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog.sqlite')


# 配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}