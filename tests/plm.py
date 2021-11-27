# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/16 17:55 
# @Author : lijun7 
# @File : plm.py
# @desc :
"""
import inspect
import os


def f2():
    return inspect.stack()


def f1():
    return f2()


if __name__ == '__main__':
    frame1 = f2()
    frame2 = inspect.stack()
    # 获取当前文件名
    file_path = frame2[0][1]
    file_name = os.path.basename(file_path)
    print(file_name)
