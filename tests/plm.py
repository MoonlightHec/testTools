# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/16 17:55 
# @Author : lijun
# @File : plm.py
# @desc :
"""
import random

purchase_info = {
    "sku": '7777777777',  # sku
    "sku_name": '产品名称',  # 产品名称
}
print("ssss  %s sss %s".replace('%s', '{}').format(*purchase_info.values()))
