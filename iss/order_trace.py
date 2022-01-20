# -*- coding: utf-8 -*-
# @Time : 2022/1/14 14:40
# @Author : sakura
# @File : order_trace.py
# @desc :
import collections

import requests


class OrderTrace:
    def __init__(self):
        self.url = 'http://10.4.4.38:7004'

    def stock_info_change_data(self, sku, biz_sn=None, stock_code=None, owner_code=None, stock_type=None):
        """
        库存轨迹：查询单据号超过2条的数据
        :param sku:产品编码
        :param biz_sn:单据号
        :param stock_code:仓库编码
        :param owner_code:货主编码
        :param stock_type:库存类型
        :return:
        """
        url = '/stock_info_change_data'
        self.url = self.url + url
        payload = {
            "page": 1,
            "limit": 90,
            "month": 12,
            "biz_sn": biz_sn,
            "sku": sku,
            "stockCode": stock_code,
            "ownerCode": owner_code,
            "stockType": stock_type
        }
        response = requests.get(self.url, params=payload).json()

        data_lst = response['data']

        biz_sn_lst = []
        for data in data_lst:
            biz_sn_lst.append(data['biz_sn'])

        biz_sn_dict = dict(collections.Counter(biz_sn_lst))
        # 展现重复单据和重复次数
        print({key: value for key, value in biz_sn_dict.items() if value > 1})


if __name__ == '__main__':
    orderTrace = OrderTrace()
    orderTrace.stock_info_change_data(sku='495062802')
