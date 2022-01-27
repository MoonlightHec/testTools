# -*- coding: utf-8 -*-
# @Time : 2022/1/27 09:38
# @Author : sakura
# @File : config.py
# @desc :
class Config:
    DEBUG = False
    SECRET_KEY = 'TPmi4aLWRbyVq8zu9v82dWYW1'
    TEMPLATES_AUTO_RELOAD = True


class DevConfig(Config):
    IP = '127.0.0.1'
    PORT = 5000
    DEBUG = True


class ProConfig(Config):
    IP = '10.8.42.152'
    PORT = 8081
