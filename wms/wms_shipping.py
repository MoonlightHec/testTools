# -*- coding: utf-8 -*-
# @Time : 2021/12/6 16:19
# @Author : lijun
# @File : shipping.py
# @desc : wms发货流程
import logging
import re
import time

from requests import ReadTimeout

from app.log.mLogger import logger
from tools.DbTools import DbTools
from tools.get_session import LoginSession


class WMSShipping:
    def __init__(self, order_sn):
        self.order_sn = order_sn
        prepare_info = self.get_prepare_info()
        self.prepare_id = prepare_info[0]
        self.stock_id = prepare_info[1]
        self.serial_no = prepare_info[2]
        self.prepare_goods = prepare_info[3]
        self.prepare_goods_id = prepare_info[4]
        self.express_track_no = f'LI{int(time.time())}'
        self.express_info_id = prepare_info[5]
        self.step = 0
        self.session = LoginSession(app_name='wms').session

    def get_prepare_info(self):
        """
        获取配货信息
        :return:
        """
        db = DbTools('wms')
        slq = "SELECT id,stock_id, serial_no, prepare_goods, prepare_goods_id, express_info_id FROM " \
              "prepare_goods_package WHERE order_no = '%s';"
        prepare_info = db.execute_sql(slq, self.order_sn)[0]
        del db
        return prepare_info

    def check_track_no(self):
        """
        跟踪号补录检查
        :return:
        """
        url = "http://wms.hqygou.com/track_no_makeup/check_one"
        payload = {
            "type": "1",
            "keyword": self.serial_no,
            "track_no": self.express_track_no,
            "express_id": "",
            "fileName": ""
        }
        res = self.session.post(url=url, data=payload)
        return res

    def add_track_no(self):
        """
        跟踪号补录
        :return:
        """
        url = "http://wms.hqygou.com/track_no_makeup/add_one"
        payload = {
            "add_type": "1",
            "keyword": self.serial_no,
            "is_change": "1",
            "express": "",
            "new_express_track_no": self.express_track_no
        }
        return self.session.post(url=url, data=payload)

    def picking_confirm(self):
        """
        捡货确认
        :return:
        """
        # 分配货位库存
        self.session.get("http://wms.hqygou.com/daemon/picking_order_queue/execAssignPickOrder/1755/1/1")

        # 捡货确认
        url = "http://wms.hqygou.com/picking_confirm/confirm_out"
        payload = {
            "package_num[]": "1",
            "prepare_goods_id": self.prepare_goods_id,
            "package_index": "1",
            "isReclaim_1": "1",
            "package_weight_1": "1.500",
            "package_product1[]": "148786003",
            "package_confirm_num1[]": "1",
            "express_code": "CAEXPZYTS",
            "track_type": "a",
            "track_no": "",
            "is_cod": "1",
            "business_department": "4",
            "weight_max": "5.000",
            "weight": "1.5",
            "sku": "148786003",
            "click_count": "1",
            "prepare_goods_no": self.prepare_goods
        }
        res = self.session.post(url=url, data=payload)
        logger.info("捡货确认结果:{}".format(res))
        return res

    def package_scan(self):
        """
        包装扫描
        :return:
        """
        url = "http://wms.hqygou.com/package_scan/scan"
        payload = {
            "serial_no": self.serial_no,
            "packers": "QC10"
        }
        res = self.session.post(url=url, data=payload)
        logger.info("包裹扫描结果:{}".format(res))
        return res

    def label_package_deal(self):
        """
        1.邮递标签打印
        2.添加包裹数据
        :return:
        """
        db = DbTools('wms')
        # 邮递标签打印
        label_sql = "UPDATE prepare_goods_package SET `status`=2,label_printer='lijun7' WHERE prepare_goods='%s';"
        db.execute_sql(label_sql, self.prepare_goods)
        # 添加包裹数据
        package_sql = "INSERT INTO sync_package_to_lms(serial_no,package_id,express_info_id,shipping_fee_count," \
                      "create_time ) VALUES('%s','%s','%s','200',CURRENT_TIMESTAMP());"
        db.execute_sql(package_sql, self.serial_no, self.prepare_id, self.express_info_id)
        del db
        logger.info("邮递标签打印,添加包裹数据成功")

    def pda_scan(self):
        """
        pda扫描
        :return:
        """
        url = "http://wms.hqygou.com/interface/devices/device_wince/sortingAction"
        payload = {
            "track_no": self.express_track_no,
            "ResponseTextType": "xml",
            "version": "201705031030",
            "username": "liujian001",
            "password": "123456",
            "stock_id": "1755",
            "stock_code": "ZQ01",
            "area": "8",
            "area_id": "8",
            "stock_yun_code": "SJ003-253",
        }
        scan = self.session.get(url=url, params=payload)
        res_scan = re.findall('<Msg>(.*?)</Msg>', scan.text)[0]
        # 同步数据到lms
        to_lms = self.session.get("http://wms.hqygou.com/daemon/wms_to_lms/smallPackageSubmittedDataToLms")
        res_lms = re.findall('<br/>(.*?)<br/><meta', to_lms.text)[0]
        logger.info("pda扫描结果:{},同步数据到lms结果:{}".format(scan.text, res_lms))
        return scan, to_lms

    def get_lms_shipping(self):
        """
        接收lms发货数据
        :return:
        """
        try:
            return self.session.get("http://wms.hqygou.com/mq_daemon/lms_queue/shippingPackageConsumerQueue",
                                    timeout=30)
        except ReadTimeout:
            return "接收lms发货数据超时，可直接查看wms包裹出库记录"


if __name__ == '__main__':
    shipping = WMSShipping('U2112241640329643')
    # 1.跟踪号补录
    # print(shipping.add_track_no().text)
    # 捡货确认
    # print(shipping.picking_confirm())
    # 包装扫描
    # print(shipping.package_scan())
    # 打印邮递标签+添加包裹数据
    # shipping.label_package_deal()
    # pda扫描并同步到lms
    shipping.pda_scan()
