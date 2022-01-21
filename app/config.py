# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/2 14:47 
# @Author : lijun
# @File : config.py
# @desc :
"""

import configparser
import os


# 配置环境ip地址 mac com
cf = configparser.ConfigParser()
root_dir = os.path.dirname(os.path.abspath(__file__))
cf.read(f'{root_dir}/config.ini', encoding='utf-8')

host = dict(cf.items('com'))
host_url = f"http://{host['ip']}:{host['port']}"
