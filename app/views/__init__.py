# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/30 16:05 
# @Author : lijun
# @File : __init__.py.py
# @desc : 初始化app
"""
from flask import Blueprint, render_template

com = Blueprint(
    'com',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@com.route('/')
def home():
    """
    根路径访问oms首页
    :return:
    """
    return render_template('oms_create_order.html')


