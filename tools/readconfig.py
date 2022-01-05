# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/19 10:18 
# @Author : lijun
# @File : myRabbitMQ.py
# @desc : 读取配置文件
"""
import configparser
import os


class ReadConfig:
    def __init__(self, config_path, section):
        # 获取当前文件ReadConfig.py绝对路径
        root_dir = os.path.dirname(os.path.abspath(__file__))
        self.cf = configparser.ConfigParser()
        self.cf.read(root_dir + config_path, encoding='utf-8')
        self.section = section

    def get_secs(self):
        """
        获取所有section
        :return:
        """
        return self.cf.sections()

    def get_options(self):
        """
        获取section的所有键
        :param section:
        :return:
        """
        try:
            return self.cf.options(self.section)
        except configparser.NoSectionError:
            print('Section：{}不存在'.format(self.section))

    def get_items(self):
        """
        获取section的所有键值对
        :param section:
        :return:
        """

        try:
            return self.cf.items(self.section)
        except configparser.NoSectionError:
            print('Section：{}不存在'.format(self.section))

    def get_value(self, key):
        """
        获取section中key的值
        :param section:
        :param key: 想要获取值的key
        :return:
        """
        try:
            return self.cf.get(self.section, key)
        except configparser.NoSectionError:
            print('Section：{}不存在'.format(self.section))
        except configparser.NoOptionError:
            print('Option：{}不存在'.format(key))


if __name__ == '__main__':
    rc = ReadConfig("/db_config.ini", "OMS")
    print(rc.get_secs())
    print(rc.get_options())
    print(rc.get_items())
    print(rc.get_value("host1"))
