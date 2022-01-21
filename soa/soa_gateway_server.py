# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/8 18:09 
# @Author : lijun
# @File : soa_gateway.py
# @desc : soa对外部系统gateway接口
"""
import requests
from flask import json

from app.log.mLogger import logger


def preview(response):
    return json.dumps(response, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)


gateway_config = {
    "token": "9988830f2e3c20e61948653d0697bbff",
    "url": "http://soa-gateway.gw-ec.com"
}


class SoaGatewayServer:
    def __init__(self):
        self.url = '{}/gateway/'.format(gateway_config["url"])
        self.headers = {"Content-Type": "application/json"}
        self.data = {
            "header": {
                "service": None,
                "method": None,
                "domain": "",
                "version": "1.0.0",
                "tokenId": gateway_config['token']
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
        return response.json()


if __name__ == '__main__':
    gateway = SoaGatewayServer()
    print(gateway.after_risk('P211028013287162412PVC'))
