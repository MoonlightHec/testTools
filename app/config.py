# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/2 14:47 
# @Author : lijun7 
# @File : config.py
# @desc :
"""
# ip地址
from flask import logging

host = {
    'ip': '10.8.34.218',
    'port': '8081'
}
host_url = f"http://{host['ip']}:{host['port']}"