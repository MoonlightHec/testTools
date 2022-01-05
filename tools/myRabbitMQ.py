# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/19 9:56 
# @Author : lijun
# @File : MyRabbitMQ.py
# @desc : 获取MQ
"""
import pika

from tools.readconfig import ReadConfig


class RabbitMQ:
    def __init__(self, name):
        self.rc = ReadConfig("/mq_config.ini", name.upper())

    def get_connection(self):
        """
        获取mq连接
        :return:
        """
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.rc.get_value('host'),
                port=int(self.rc.get_value('port')),
                credentials=pika.PlainCredentials(self.rc.get_value('user'), self.rc.get_value('password'))
            )
        )
        return connection
