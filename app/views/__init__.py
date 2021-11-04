# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/30 16:05 
# @Author : lijun7 
# @File : __init__.py.py
# @desc :
"""

from flask import Blueprint, render_template

from app.config import host_url

com = Blueprint(
    'com',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@com.route('/')
def home():
    return render_template('index.html', url=host_url)


@com.route('/index.html')
def index():
    return render_template('index.html', url=host_url)
