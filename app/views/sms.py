# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/4 15:52 
# @Author : lijun
# @File : sms.py
# @desc :
"""
from flask import Blueprint, render_template


sms = Blueprint(
    'sms',
    __name__,
    template_folder='templates',
    static_folder='static'
)


