# -*- coding: utf-8 -*-
# @Time : 2022/1/27 10:25
# @Author : sakura
# @File : __init__.py
# @desc :

from flask import render_template, Flask

from app.config import ProConfig, DevConfig
from app.views import com
from app.views.oms import oms
from app.views.sms import sms
from app.views.soa import soa
from app.views.webmin import webmin
from app.views.wms import wms

app = Flask(__name__)


def register_blueprints():
    """注册蓝图"""
    app.register_blueprint(com)
    app.register_blueprint(oms, url_prefix='/oms')
    app.register_blueprint(soa, url_prefix='/soa')
    app.register_blueprint(sms, url_prefix='/sms')
    app.register_blueprint(wms, url_prefix='/wms')
    app.register_blueprint(webmin, url_prefix='/webmin')


def app_config(env='product'):
    if env == 'product':
        env_config = ProConfig()
    elif env == 'develop':
        env_config = DevConfig()
    return env_config


def create_app(env='product'):
    """初始化app的各项功能,生产、组装app的工厂"""
    env_config = app_config(env)

    # 下两行配置修改html不需要重启后台
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = env_config.TEMPLATES_AUTO_RELOAD
    app.config["SECRET_KEY"] = env_config.SECRET_KEY
    app.config['DEBUG'] = env_config.DEBUG

    # 设置全局函数给html传递host参数
    # --host=10.8.42.152 --port=8081
    app.add_template_global(f"http://{env_config.IP}:{env_config.PORT}", name="host")

    register_blueprints()
    return app


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('505.html'), 500
