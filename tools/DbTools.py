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


class DbTools:
    def __init__(self, name):
        # 获取当前文件db.py绝对路径
        db_path = os.path.dirname(os.path.abspath(__file__))
        with open(f'{db_path}/db_config.json', 'r', encoding='utf-8') as db_stream:
            datas = json.load(db_stream)

        db_config = datas[name.upper()]
        self.connect = pymysql.connect(**db_config)
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.cursor.close()
        self.connect.close()

    def execute_sql(self, mysql, *args):
        self.cursor.execute(mysql % args)
        result = self.cursor.fetchall()
        self.connect.commit()
        logger.info("execute_sql影响数据：{}".format(self.cursor.rowcount))
        return result


if __name__ == '__main__':
    db = DbTools('plm')
    slq = "SELECT * FROM t_sys_user WHERE id = '%s'"
    s = db.execute_sql(slq, 27228)
    del db
    print(s)

