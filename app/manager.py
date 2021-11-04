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
from app.views.soa import soa

app = Flask(__name__)

app.register_blueprint(com)
app.register_blueprint(oms, url_prefix='/oms')
app.register_blueprint(soa, url_prefix='/soa')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(505)
def internal_server_error(e):
    return render_template('505.html'), 505


if __name__ == '__main__':
    # --host=10.8.34.218 --port=8081

    app.run(host=host['ip'], port=['port'], debug=True)
