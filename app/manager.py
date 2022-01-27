# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/30 15:16
# @Author : lijun
# @File : __init__.py
# @desc :
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
