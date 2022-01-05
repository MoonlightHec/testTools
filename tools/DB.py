# -*- coding: utf-8 -*-
# @Time : 2022/1/5 16:05
# @Author : lijun
# @File : DB.py
# @desc :
import pymysql

from tools.readconfig import ReadConfig


class DB:
    """
    使用上下文管理器连接数据库
    """

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
            db_config['cursorclass'] = pymysql.cursors.DictCursor
            return db_config

    def query(self, mysql, *args):
        """
        查询sql
        :param mysql:
        :param args:
        :return:
        """
        self.cursor.execute(mysql % args)
        result = self.cursor.fetchall()
        return result

    def update(self, mysql, *args):
        """
        执行sql,增、删、改
        :param mysql:
        :param args:
        :return:
        """
        self.cursor.execute(mysql % args)
        self.cursor.fetchall()
        self.connect.commit()
        if self.cursor.rowcount:
            return True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connect.close()


if __name__ == '__main__':
    with DB('plm') as db:
        a = db.query("select * from t_bom_record where sku='206148101';")
        b = [i['spu'] for i in a]
        print(b)
