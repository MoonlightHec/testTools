# -*- coding: utf-8 -*-
# @Time : 2021/12/6 18:45
# @Author : lijun
# @File : lms_shipping.py
# @desc :
import requests

from tools.DbTools import DbTools
from tools.get_session import LoginSession


class LMSShipping:
    def __init__(self, order_sn):
        prepare_info = self.get_prepare_info()
        self.order_sn = order_sn
        self.order_number = prepare_info[0]

    def get_prepare_info(self):
        """
        获取发货信息
        :return:
        """
        db = DbTools('lms1')
        slq = "select order_number from orders where oms_number='%s'"
        prepare_info = db.execute_sql(slq, self.order_sn)[0]
        del db
        return prepare_info

    def pda_create_box(self):
        """
        pda装箱
        :return:
        """
        url = "http://lms.hqygou.com/outapi/Box/create.php"
        payload = {
            "identifier": "f69c9c0709dc0807e700c0b83481c94d",
            "username": "lishenping",
            "password": "123456",
            "order_number": self.order_number,
            "is_first": "1"
        }
        session = LoginSession.get_lms_session()
        return session.post(url=url, data=payload)


if __name__ == '__main__':
    shipping = LMSShipping("U2112061638776430")
    print(shipping.pda_create_box().text)
