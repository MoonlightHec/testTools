# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/30 16:57 
# @Author : lijun
# @File : soa.py
# @desc :
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.config import host_url
from app.log.mLogger import logger
from app.server.tools_soa import create_soa_order
from soa.soa_gateway_server import SoaGatewayServer

soa = Blueprint(
    'soa',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@soa.route('/soa_checkout_order', methods=['GET', 'POST'])
def soa_index():
    """
    soa首页（checkout订单）
    :return:
    """
    return render_template('soa_checkout_order.html', url=host_url)


@soa.route('/soa_gateway', methods=['GET', 'POST'])
def soa_risk():
    """
    事后风控页面
    :return:
    """
    return render_template('soa_gateway.html', url=host_url)


@soa.route('/soa_xxx', methods=['GET', 'POST'])
def soa_xxx():
    """
    添加soa新页面
    :return:
    """
    return render_template('soa_xxx.html', url=host_url)


@soa.route('/soa_checkout_order/<path:cashier>', methods=['GET', 'POST'])
def create_order_redirect(cashier):
    """
    创建订单后重定向到soa页面，防止刷新二次提交表单
    :param cashier:
    :return:
    """
    return render_template('soa_checkout_order.html', url=host_url, cashier=cashier)


@soa.route('/soa_gateway/<path:res>', methods=['GET', 'POST'])
def soa_gateway_redirect(res):
    """
    重定向到soa_gateway页面
    :param res:
    :return:
    """
    return render_template('soa_gateway.html', url=host_url, after_risk_result=res)


@soa.route('/create_order', methods=['GET', 'POST'])
def create_order():
    """
    checkout收银台
    :return:
    """
    # 将获取到的表单数据转化为dict
    front_params = request.form.to_dict()
    logger.info("checkout收银台:form表单数据 {}".format(front_params))
    cashier = create_soa_order(front_params)
    return redirect(url_for('soa.create_order_redirect', cashier=cashier))


@soa.route('/soa_gateway/after_risk', methods=['GET', 'POST'])
def after_risk():
    """
    事后风控
    :return:
    """
    front_params = request.form.to_dict()
    logger.info("checkout收银台:form表单数据 {}".format(front_params))
    gateway = SoaGatewayServer()
    res = gateway.after_risk(front_params["pay-sn"])
    return redirect(url_for('soa.soa_gateway_redirect', res=res))
