# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/4 16:03 
# @Author : lijun
# @File : wms.py
# @desc :
"""
from flask import Blueprint, render_template

wms = Blueprint(
    'wms',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@wms.route('/test', methods=['GET', 'POST'])
def soa_index():
    """
    soa首页（checkout订单）
    :return:
    """
    return render_template('404.html')
