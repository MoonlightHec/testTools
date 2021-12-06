# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/16 17:55 
# @Author : lijun7 
# @File : plm.py
# @desc :
"""
import inspect
import os


def fun(input_num):
    str_decimal = str(input_num).split(".")
    if len(str_decimal[1]) >= 6:
        decimal = str_decimal[1][:6]
        result = float(f'{str_decimal[0]}.{decimal}')
    else:
        result = input_num
    return result


if __name__ == '__main__':
    print(fun(10.1234534232))
