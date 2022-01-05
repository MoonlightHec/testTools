# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/15 10:43 
# @Author : lijun
# @File : encrypt.py
# @desc :
"""
import hashlib

from app.log.mLogger import logger


def md5(string):
    m = hashlib.md5()
    m.update(string.encode("utf8"))
    logger.info("加密前：【{}】,加密后：【{}】".format(string, m.hexdigest()))
    return m.hexdigest()


def sha256(string):
    m = hashlib.sha256()
    m.update(string.encode("utf8"))
    logger.info("加密前：【{}】\n加密后：【{}】".format(string, m.hexdigest()))
    return m.hexdigest()


if __name__ == '__main__':
    str = 'huangjieyin@zaful.com1638531981xDHXibIJKtFhEjjOInxkoEjupo5ZUIw2'
    print(md5(str))
