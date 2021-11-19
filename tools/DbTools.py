# _*_ coding: utf-8 _*_
"""
# @Time : 2021/8/27 9:10 
# @Author : lijun7 
# @File : DbTools.py
# @desc :
"""
import os

import pymysql
from flask import json

from app.log.mLogger import logger
from tools.readconfig import ReadConfig


class DbTools:
    def __init__(self, name):
        # 读取配置文件
        rc = ReadConfig('/db_config.ini', name.upper())
        datas = rc.get_items()
        # 元组转换成字典
        db_config = dict(datas)
        # port转化成int型
        db_config['port'] = int(db_config['port'])
        self.connect = pymysql.connect(**db_config)
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.cursor.close()
        self.connect.close()

    def execute_sql(self, mysql, *args):
        self.cursor.execute(mysql % args)
        result = self.cursor.fetchall()
        self.connect.commit()
        logger.info("execute_sql({})影响数据：{}".format(mysql, self.cursor.rowcount))
        return result


if __name__ == '__main__':
    db = DbTools('plm')
    slq = "SELECT * FROM t_sys_user WHERE id = '%s'"
    s = db.execute_sql(slq, 27228)
    del db
    print(s)
