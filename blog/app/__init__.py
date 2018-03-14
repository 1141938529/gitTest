from app.config import config
from flask import Flask, render_template
from app.extensions import config_extensions
from app.views import config_blueprint



# 配置错误处理
def config_errorhandler(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html')

# 封装一个函数，创建app
def create_app(config_name):
    # 生成app实例
    app = Flask(__name__)

    # 读取配置
    app.config.from_object(config.get(config_name) or config['default'])

    # 执行额外的初始化操作
    config[config_name].init_app(app)

    # 添加扩展
    config_extensions(app)

    # 配置蓝本
    config_blueprint(app)
    # 配置错误页面
    config_errorhandler(app)
    # 返回app
    return app


