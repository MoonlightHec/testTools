# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/30 15:16
# @Author : lijun7
# @File : __init__.py
# @desc :
"""
from flask import Flask, render_template

from app.config import host
from app.views import com
from app.views.oms import oms
from app.views.sms import sms
from app.views.soa import soa
from app.views.wms import wms

app = Flask(__name__)

# 下两行配置修改html不需要重启后台
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'

app.register_blueprint(com)
app.register_blueprint(oms, url_prefix='/oms')
app.register_blueprint(soa, url_prefix='/soa')
app.register_blueprint(sms, url_prefix='/sms')
app.register_blueprint(wms, url_prefix='/wms')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('505.html'), 500


if __name__ == '__main__':
    # --host=10.8.42.152 --port=8081

    app.run(host=host['ip'], port=['port'], debug=False)
