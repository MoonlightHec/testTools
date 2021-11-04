# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/2 14:44 
# @Author : lijun7 
# @File : mLogger.py
# @desc :
"""
import logging

logging.basicConfig(
    format='%(asctime)s - [ %(filename)s---%(funcName)s---line:%(lineno)d] - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)
logger = logging.getLogger(__name__)
