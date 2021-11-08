# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/4 16:03 
# @Author : lijun7 
# @File : wms.py
# @desc :
"""
from flask import Blueprint, render_template

from app.config import host_url

wms = Blueprint(
    'wms',
    __name__,
    template_folder='templates',
    static_folder='static'
)
