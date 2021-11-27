# _*_ coding: utf-8 _*_
"""
# @Time : 2021/8/27 9:10 
# @Author : lijun7 
# @File : DbTools.py
# @desc :
"""

import pymysql

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
        """
        使用上面的写法更简洁
        （**）会把接收到的参数存入一个字典
        在函数调用的时候，Python解释器自动按照参数位置和参数名把对应的参数传进去。
        self.connect = pymysql.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            db=db_config['db'],
            charset=db_config['charset']
        )
        """
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
    db = DbTools('iss')
    slq = "SELECT * FROM iss_1.biz_base_info LIMIT 1"
    s = db.execute_sql(slq)
    del db
    print(s)
