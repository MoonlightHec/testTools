# _*_ coding: utf-8 _*_
"""
# @Time : 2021/8/27 9:10 
# @Author : lijun
# @File : DbTools.py
# @desc :
"""

import pymysql

from app.log.mLogger import logger
from tools.readconfig import ReadConfig


class DbTools:
    def __init__(self, name):
        self.name = name
        self.connect = pymysql.connect(**self.read_config())
        self.cursor = self.connect.cursor()

    def read_config(self):
        # 读取配置文件
        rc = ReadConfig('/db_config.ini', self.name.upper())
        datas = rc.get_items()
        if datas:
            # 元组转换成字典
            db_config = dict(datas)
            # port转化成int型
            db_config['port'] = int(db_config['port'])
            return db_config

    def __del__(self):
        try:
            self.cursor.close()
            self.connect.close()
        except AttributeError:
            logger.info(f"{self.name}数据库未连接成功，无需关闭")
            return

    def execute_sql(self, mysql, *args):
        self.cursor.execute(mysql % args)
        self.connect.commit()
        result = self.cursor.rowcount
        logger.info("execute_sql({}),参数：【{}】影响数据：{}".format(mysql, *args, result))
        return result

    def query(self, mysql, *args):
        self.cursor.execute(mysql % args)
        result = self.cursor.fetchall()
        return result


if __name__ == '__main__':
    db = DbTools('iss')
    slq = "SELECT * FROM iss_1.biz_base_info LIMIT 1"
    s = db.query(slq)
    del db
    print('我的{name}')
