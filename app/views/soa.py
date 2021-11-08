# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/30 16:57 
# @Author : lijun7 
# @File : soa.py
# @desc :
"""
from flask import Blueprint, render_template, request, redirect, url_for

from app.config import host_url
from app.server.tools_soa import create_soa_order

soa = Blueprint(
    'soa',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@soa.route('/soa_checkout_order', methods=['GET', 'POST'])
def soa_index():
    return render_template('soa_checkout_order.html', url=host_url)


@soa.route('/soa_xxx', methods=['GET', 'POST'])
def soa_xxx():
    return render_template('soa_xxx.html', url=host_url)


@soa.route('/create_order', methods=['GET', 'POST'])
def create_order():
    print("header {}".format(request.headers))
    print("args ", request.args)
    print("form {}".format(request.form.to_dict()))
    # 将获取到的表单数据转化为dict
    user_order_info = request.form.to_dict()
    cashier = create_soa_order(user_order_info)
    # return render_template('soa_model.html', url=host_url, cashier=cashier)
    return redirect(url_for('soa.create_order_redirect', cashier=cashier))


@soa.route('/soa_checkout_order/<path:cashier>', methods=['GET', 'POST'])
def create_order_redirect(cashier):
    """
    创建订单后重定向到soa页面，防止刷新二次提交表单
    :param cashier:
    :return:
    """
    return render_template('soa_checkout_order.html', url=host_url, cashier=cashier)
