# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/15 10:43 
# @Author : lijun7 
# @File : encrypt.py
# @desc :
"""
import hashlib

import phpserialize
from itsdangerous import Serializer

from app.log.mLogger import logger


class Encrypt:
    def __init__(self, string):
        self.string = string

    def md5(self):
        m = hashlib.md5()
        m.update(self.string.encode("utf8"))
        logger.info("加密前：【{}】,加密后：【{}】".format(self.string, m.hexdigest()))
        return m.hexdigest()

    def sha256(self):
        m = hashlib.sha256()
        m.update(self.string.encode("utf8"))
        logger.info("加密前：【{}】\n加密后：【{}】".format(self.string, m.hexdigest()))
        return m.hexdigest()


if __name__ == '__main__':
    str = Encrypt('123456')
    print(str.md5())
