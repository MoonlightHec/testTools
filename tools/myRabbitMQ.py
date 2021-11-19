# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/19 9:56 
# @Author : lijun7 
# @File : MyRabbitMQ.py
# @desc :
"""
from tools.readconfig import ReadConfig


class RabbitMQ:
    def __init__(self, name):
        rc = ReadConfig("/mq_config.ini", name.upper())
