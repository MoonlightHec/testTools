# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/15 16:59 
# @Author : lijun
# @File : format.py
# @desc : 格式化各种数据
"""
import collections
import json

import phpserialize

from app.log.mLogger import logger


def serialize(string):
    """
    PHP序列化数据,如果字符串有中文转换的Unicode会不准
    :return:
    """
    serialized = phpserialize.dumps(string, charset='utf-8')
    logger.info("PHP序列化前：【{}】\n序列化后：【{}】".format(string, serialized))
    return serialized


def bejson(json_string):
    """
    json按键排序
    :return:
    """
    # 方法一
    sort_movies = collections.OrderedDict(sorted(json_string.items(), key=lambda x: x[0], reverse=False))
    dict_movies = dict(sort_movies)
    return dict_movies
    # 方法二
    # format_json = json.dumps(json_string, sort_keys=True).encode('utf-8').decode("unicode_escape")
    # format_json = json.dumps(json_string, sort_keys=True)
    # return json.loads(format_json)



if __name__ == '__main__':
    pass
