# -*- coding: utf-8 -*-
# @Time : 2021/12/24 17:42
# @Author : lijun
# @File : joint_order.py
# @desc : 联合订单推到oms,工具里暂时没加

import requests

from tools.WebminObj import WebminObj
from tools.encrypt import md5


class JointOrder:

    def __init__(self, order_sn):
        self.order_sn = order_sn

    def zf_push_mq(self):
        """
        ZF推送联合订单到MQ
        :return:
        """
        url = 'http://www.pc-zaful-master-php5.fpm.egomsl.com/eload_admin/crontab/xcmq/warehouse/OrderToOmsApi.php?order_sn=%s'
        response = requests.get(url % self.order_sn)
        print(response.text)

    def oms_deal(self, step=0):
        """
        联合订单导单三部曲
        :return:
        """
        webmin = WebminObj('oms')
        if step == 1:
            # oms导入脚本
            webmin.run_script('soa_mq_oms_received')
        elif step == 2:
            webmin.run_script('soa_order_into_mq', self.order_sn, md5(self.order_sn)[:2])
        elif step == 3:
            webmin.run_script('get_soa_mq_into_oms')
        else:
            return


if __name__ == '__main__':
    joint_order = JointOrder('U2112240257259056')
    # joint_order.zf_push_mq()
    joint_order.oms_deal(2)

