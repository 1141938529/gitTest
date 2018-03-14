from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class



# 创建扩展对象
bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
db = SQLAlchemy()
migrate = Migrate(db=db)
login_manager = LoginManager()
photos = UploadSet('photos', IMAGES)

# 初始化
def config_extensions(app):
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)


    # 配置login_manager
    # 配置登录的端点
    login_manager.login_view = 'user.login'

    login_manager.login_message = '需要登录才能访问'

    login_manager.session_protection = 'strong'

    # 配置文件上传
    configure_uploads(app,photos)

    patch_request_class(app, size=None)