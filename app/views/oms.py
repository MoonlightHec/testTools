# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/30 16:01 
# @Author : lijun7 
# @File : oms.py
# @desc :
"""
from flask import Blueprint, render_template, request

from app.config import host_url

oms = Blueprint(
    'oms',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@oms.route('/oms_model.html',methods=['GET', 'POST'])
def oms_model():
    return render_template('oms_model.html', host=host_url)


@oms.route("/create_order", methods=["GET", "POST"])
def get_order_info():
    """
    oms创建订单
    :return:
    """
    print("header {}".format(request.headers))
    print("args ", request.args)
    print("form {}".format(request.form.to_dict()))
    # 将获取到的表单数据转化为dict
    user_order_info = request.form.to_dict()
    # order_sn = create_oms_order(user_order_info)
    order_sn = 'ooooooooooooooo'
    if order_sn:
        return render_template('/oms_model.html', cashier_url=user_order_info)
    return "创建失败"
