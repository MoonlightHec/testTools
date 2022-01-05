# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/11 11:54 
# @Author : lijun
# @File : Airwallex.py
# @desc :
"""
import time

import requests
from flask import json


class Airwallex:
    def __init__(self):
        self.allDomains = {
            'apiDomain': 'https://api-demo.airwallex.com',
            'fileDomain': 'https://files-demo.airwallex.com',
            'paDomain': 'https://pci-api-demo.airwallex.com',
            'isDomain': 'https://pci-api-demo.airwallex.com'
        }
        self.client = {
            'clientId': '4OuJUnXeQuGF9jZuEhl8-Q',
            'apiKey': '6af583d04f8fdd4a1537460093b07d974fc340f0c787ba148d8d2d1785bb69c89078622c2ea677b9862887fb2f0ce91e',
        }
        self.headers = {
            "Authorization": "Bearer {}".format(self.login()),
            "Content-Type": "application/json",
        }

    def login(self):
        url = '{}/api/v1/authentication/login?api_key={}&client_id={}'.format(self.allDomains['paDomain'], self.client['apiKey'], self.client['clientId'])
        headers = {
            'Content-Type': 'application/json',
            'x-client-id': self.client['clientId'],
            'x-api-key': self.client['apiKey']
        }
        res = requests.post(url=url, headers=headers)
        token = res.json().get('token')
        return token

    def get_payment(self, payment_intent_id):
        """
        查询支付记录
        :param payment_intent_id:
        :return:
        """
        url = '{}/api/v1/pa/payment_intents/{}'.format(self.allDomains['paDomain'], payment_intent_id)
        res = requests.get(url, headers=self.headers)
        self.preview(res)

    def create_refunds(self, payment_intent_id='', amount=0):
        """
        向第三方请求退款
        :param amount:
        :param payment_intent_id:
        :return: 登录不上，还没调试过
        """
        url = '{}/api/v1/pa/refunds/create'.format(self.allDomains['paDomain'])
        params = {
            "payment_intent_id": payment_intent_id,
            "reason": "Return good",
            "amount": amount,
            "request_id": int(time.time())
        }
        res = requests.get(url, headers=self.headers, params=params)
        if res.status_code == 201:
            print(res.json())
            return res

    def get_refunds(self, payment_intent_id):
        """
        查询awx退款记录
        :param payment_intent_id:
        :return:
        """
        url = '{}/api/v1/pa/refunds'.format(self.allDomains['paDomain'])
        params = {
            "payment_intent_id": payment_intent_id
        }
        res = requests.get(url, headers=self.headers, params=params)
        if res.status_code == 200:
            return res

    def preview(self, response):
        try:
            print(json.dumps(response.json(), sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))
        except AttributeError:
            print(json.dumps(response, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))

    def run_refunds(self, payment_intent_id='', result='SUCCEEDED', awx_refund_sn=None):
        """
        模拟第三方发送退款通知
        :param payment_intent_id:
        :param result:退款结果
        :param awx_refund_sn: 指定退款id
        :return:
        """
        items = self.get_refunds(payment_intent_id).json()['items']
        if awx_refund_sn:
            for item in items:
                if item['metadata']['refundSn'] == awx_refund_sn:
                    refunds_obj = item
        else:
            refunds_obj = items[0]
        self.preview(refunds_obj)
        refunds_obj['status'] = result
        data = {
            "accountId": "acct_xJ_pXQ3pOiOiGCkcSP0c7Q",
            "createdAt": "2021-08-18T00:54:49+0000",
            "data": {
                "object": refunds_obj
            },
            "id": "evt_hkdmnwcv6g1iq8mc8ik_694bm8",
            "name": "refund.succeeded",
            "version": "2020-04-30",
            "account_id": "acct_xJ_pXQ3pOiOiGCkcSP0c7Q",
            "created_at": "2021-08-18T00:54:49+0000"
        }
        if result == 'FAILED':
            data['name'] = 'refund.failed'

        url = 'http://10.40.2.52:8182/awx/notify'
        res = requests.post(url, headers=self.headers, json=data)
        if res.status_code == 200:
            print('接收退款通知成功')


if __name__ == '__main__':
    intent_id = 'int_hkdmgdk7xg4la7116ws'
    awx_pay_sn = 'U2111260125292421'
    refund_sn = 'B210923013287182905DVI'
    awx_cc = Airwallex()
    # awx_cc.get_payment(intent_id)
    # result='FAILED',result='SUCCEEDED'
    # awx_cc.run_refunds(payment_intent_id=intent_id, result='SUCCEEDED')
    print(awx_cc.preview(awx_cc.get_refunds(intent_id)))
    awx_cc.create_refunds(intent_id,0.99)