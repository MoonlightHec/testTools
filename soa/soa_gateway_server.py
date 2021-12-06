# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/8 18:09 
# @Author : lijun7 
# @File : soa_gateway.py
# @desc : soa对外部系统gateway接口
"""
import requests
from flask import json

from app.log.mLogger import logger
from soa.config import gateway_config


def preview(response):
    return json.dumps(response, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)


class SoaGatewayServer:
    def __init__(self, env='old'):
        self.env = env
        self.url = '{}/gateway/'.format(gateway_config[env]["url"])
        self.headers = {"Content-Type": "application/json"}
        self.data = {
            "header": {
                "service": None,
                "method": None,
                "domain": "",
                "version": "1.0.0",
                "tokenId": gateway_config[env]['token']
            },
            "body": None
        }

    def after_risk(self, pay_sn):
        """
        事后风控
        :param pay_sn:
        :return:
        """
        self.data["header"]["service"] = 'com.globalegrow.risk.api.core.RiskCoreService'
        self.data["header"]["method"] = 'afterRiskProcessor'
        self.data["body"] = {
            "paySn": pay_sn,
            "omsId": ""
        }
        response = requests.post(url=self.url, headers=self.headers, json=self.data)
        logger.info("事后风控调用结果：{}".format(response.json()))
        # if response.json()["header"]["success"]:
        #     return "调用成功"
        return response.json()


if __name__ == '__main__':
    gateway = SoaGatewayServer()
    print(gateway.after_risk('P211028013287162412PVC'))
