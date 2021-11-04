# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/30 16:57 
# @Author : lijun7 
# @File : soa.py
# @desc :
"""
from flask import Blueprint, render_template, request, jsonify, redirect

from app.config import host_url

soa = Blueprint(
    'soa',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@soa.route('/soa_model.html', methods=['GET', 'POST'])
def soa_index():
    return render_template('soa_model.html', url=host_url)


@soa.route('/create_order', methods=['GET', 'POST'])
def create_order():
    print("header {}".format(request.headers))
    print("args ", request.args)
    print("form {}".format(request.form.to_dict()))
    # 将获取到的表单数据转化为dict
    user_order_info = request.form.to_dict()
    # order_sn = create_oms_order(user_order_info)
    order_sn = 'https://cashier.dresslily.net/?token=O211103005362114051N3T&lang=en1'
    return render_template('soa_model.html', url=host_url, cashier=order_sn)
