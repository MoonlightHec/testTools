# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/15 16:49 
# @Author : lijun7 
# @File : Pacypay.py
# @desc :
"""

import requests
from flask import json


class Pacypay:
    def __init__(self):
        self.url = 'https://sandbox-pg.pacypay.com/'

    def get_pay_info(self, pay_sn):
        """
        获取支付请求信息
        :param pay_sn:
        :return:
        """
        url = '{}/query/transaction'.format(self.url)
        params = {
            "merchantNo": "2246",
            "tradeTimeStart": "2021-10-11 00:00:00",
            "tradeTimeEnd": "2022-10-11 00:00:00",
            "sign": "b45dc50226e63ff0b0b14979fc0bdfe8f03ed012ae55ece7ba3d029ecb700b46"
        }
        try:
            all_data = requests.get(url, params).json()
            for data in all_data["trans"]:
                if data['transactionId'] == pay_sn:
                    print(json.dumps(data, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))
        except TypeError:
            print(all_data)

    def run_refunds(self, pay_sn, refund_amount, amount, transaction_id):
        """
        模拟退款
        :return:
        """

        data = {
            "merchantNo": "2167",
            "transactionType": "Refund",
            "transactionId": pay_sn,
            "uniqueId": transaction_id,
            "refundId": "461944312336355328",
            "tradeTime": "2021-10-26 16:55:52",
            "currency": "USD",
            "amount": amount,
            "refundAmount": refund_amount,
            "refundStatus": "3",
        }
        sign = ''
        for i in sorted(data):
            sign += data[i]
        sign += '56243b13b9fa4156a6c687641343e362'
        sign = self.sha256(sign)

        url = "http://10.40.2.52:8182/pacypay/notify"
        headers = {"Content-Type": "application/json"}
        data.update({"sign": sign})
        res = requests.post(url=url, headers=headers, json=data)
        print(data)
        print(res)


if __name__ == '__main__':
    pay_cc = Pacypay()
    pay_cc.get_pay_info('P211103005378141404WCN')
    # pay_cc.run_refunds(pay_sn='P211103005378141404WCN', refund_amount='0.15', amount='38.11', transaction_id='2167211131414638182')
