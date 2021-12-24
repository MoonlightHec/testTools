# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/15 17:21 
# @Author : lijun7 
# @File : order_all_process.py
# @desc :
"""
import re

import requests

from app.log.mLogger import logger
from tools.DbTools import DbTools
from tools.get_session import LoginSession


class OrderAllProcess:
    def __init__(self, order_sn):
        self.order_sn = order_sn

    def add_sku(self, sku_str_list):
        """
        添加sku到oms产品表
        :param sku_str_list:
        :return:
        """
        oms_db = DbTools('OMS')
        exist_sku = []
        succeed_sku = []
        failed_sku = []

        # 判断是否含有字母
        if re.search('[^0-9,]', sku_str_list):
            logger.info("添加sku的格式不符合：{}".format(sku_str_list))
            return "sku格式不符合！"
        sku_list = eval(sku_str_list)

        if isinstance(sku_list, int):
            sku_list = [sku_str_list]
        for sku in sku_list:
            query_sql = "SELECT * FROM oms.g_oms_goods WHERE goods_sn = '%s'"
            if oms_db.query(query_sql, sku):
                exist_sku.append(sku)
            else:
                insert_sql = "INSERT INTO oms.g_oms_goods (cat_id, goods_sn, goods_name, product_title, goods_weight, shop_price, shiji_price,goods_img, purchaser, add_time, " \
                             "is_delete, goods_state, purchase_title, volume_weight,product_distinction, goods_nature, specification, declar_cn_name, declar_en_name,declar_price, " \
                             "customs_code, battery_type, update_user, is_clearance,product_length, product_width, product_height, package_length, package_width," \
                             "package_height, batch_purchase_price, is_batch, stock_attribute, goods_type,guide_price_us, guide_price, battery_brand, battery_voltage, " \
                             "battery_current,battery_power, battery_capacity, researcher, brand_en_name, brand_code, brand_name,purchase_price_unit, pack_attribute, edit_status," \
                             " purchase_price_base, recommend_level,unit_code) VALUES (1913, '%s', 'Rhinestone Studded Edge Bikini Swimwear', 'Rhinestone Studded Edge " \
                             "Bikini Swimwear', 0.100,85.00, 75.00, 'uploads/201203/thumb-img/1332726684915-thumb-P-250665.jpg', 'lijun7', UNIX_TIMESTAMP(NOW()), 0,3," \
                             "'【手动添加】钻饰挂脖V领系带粉色分体泳衣泳装40305 粉色', 0.100, 4, '1', 1, '服装', 'Dresses', 2.00, '95030089', '', 'lijun7', 0, " \
                             "0.000000, 0.000000, 0.000000, 1.000000, 1.000000, 1.000000, 0.00, 1, 1, 1,'', '', '', '', '', '', '', '', '', '', '', 'CNY', 0, 6, 75.00000, '', '');"
                if oms_db.execute_sql(insert_sql, sku):
                    succeed_sku.append(sku)
                else:
                    failed_sku.append(sku)
        add_result = {
            "已存在的sku": exist_sku,
            "添加成功": succeed_sku,
            "添加失败": failed_sku
        }
        logger.info("添加sku到oms：{}".format(add_result))
        return add_result

    def get_picking_sn(self):
        """
        获得配货单号
        :return:
        """
        oms_db = DbTools('OMS')
        new_order_sql = "SELECT order_number_new FROM oms.o_oms_order_picking_info WHERE order_sn='%s'"
        new_order_res = oms_db.query(new_order_sql, self.order_sn)
        del oms_db
        try:
            picking_sn = new_order_res[0][0]
            return picking_sn
        except IndexError:
            return '未找到配货单，可能oms未配货'

    def wms_get_picking_order(self):
        """
        wms接收配货单
        :return:
        """
        wms_db = DbTools('WMS')
        try:
            # 查找配货单id
            id_sql = "SELECT id FROM prepare_goods WHERE  prepare_goods_no='%s'"
            picking_id = wms_db.query(id_sql, self.get_picking_sn())[0][0]
            del wms_db
            # 执行接收配货单脚本
            if picking_id:
                url = "http://wms.hqygou.com/daemon/picking_order_queue/autoCreatePackage/{}".format(str(picking_id)[-1:])
                return requests.get(url).text
        except IndexError:
            return 'oms未同步配货单'

    def site_push_order(self, site_code):
        """
        网站推送订单到oms
        :param site_code:
        :return:
        """
        url_web = "http://www.pc-{}-php5.fpm.egomsl.com/eload_admin/crontab/xcmq/order_to_oms_api.php?order_sn={}"
        web_branch = {
            "ZF": "zaful-v1223",
            "DL": "dresslily-lucky_bag",
            "RG": "master"
        }
        requests_url = url_web.format(web_branch[site_code], self.order_sn)
        logger.info("网站推送订单到oms请求链接：{}".format(requests_url))
        return requests.get(requests_url).text

    def audit_payorder(self):
        """
        审核付款单
        :return:
        """
        oms_db = DbTools('OMS')
        try:
            # 获取付款单id
            payorder_id_sql = "SELECT payment_info_id FROM f_oms_payment_info WHERE order_sn='%s'"
            payment_info_id = oms_db.query(payorder_id_sql, self.order_sn)[0][0]
            del oms_db

            # 审核付款单
            url = 'http://oms.hqygou.com/finance/payorder/payorderaudit/'
            login = LoginSession('oms')
            data = {"payment_info_id": payment_info_id, "status": 1}
            return login.session.post(url=url, data=data).json()
        except IndexError:
            return '付款单不存在'

    def deal_question(self):
        """
        处理订单问题
        :return:
        """
        oms_db = DbTools('OMS')
        # 处理地址异常问题，否则要在wos处理
        address_sql = "UPDATE o_oms_order_question SET order_question_status=3 WHERE order_sn='%s' AND order_question_type_id=2;"
        oms_db.execute_sql(address_sql, self.order_sn)

        # 处理其他问题
        other_sql = "SELECT order_question_id FROM oms.o_oms_order_question  WHERE order_sn='%s';"
        question_ids = oms_db.query(other_sql, self.order_sn)
        # 问题无需处理操作请求接口
        url = "http://oms.hqygou.com/order/process/process"
        login = LoginSession('oms')
        for question_id in question_ids:
            data = {
                "order_question_id": question_id[0],
                "order_question_process_id": 3,
                "not_send_email": 1
            }
            login.session.post(url, data=data).json()
        # 检查问题是否都处理了
        check_sql = "SELECT order_question_id FROM oms.o_oms_order_question WHERE order_sn='%s' AND order_question_status!=3;"
        if oms_db.query(check_sql, self.order_sn):
            return "有问题处理失败，请手动处理"
        return '全部问题处理成功！'

    def oms_piking_order(self, sku=None, stock_id=0, express_id=0):
        """
        oms订单配货
        :return:
        """
        # 获取配货订单信息
        oms_session = LoginSession('oms')
        order_data_url = "http://oms.hqygou.com/order/picking/getorderjsondata"
        order_data = {
            "order_sn": self.order_sn,
            "stock_id": stock_id
        }
        try:
            res = oms_session.session.post(order_data_url, order_data).json()
            goods_data = res['data']['goods']
        except KeyError:
            return res

        # 发起配货请求
        # 获取请求参数
        picking_data = {
            "is_temp": 0,
            "is_remote": 0,
            "is_from_picking": 1,
            "stock_id": stock_id,
            "express_id": express_id,
            "order_sn": self.order_sn,
            "goods_weight": 0,
            "express_list": "加拿大专线(FZ)",
            "overweight": 0,
            "first_declare_total": 0,
            "last_declare_total": None
        }
        for goods in goods_data:
            picking_goods_data = {
                f"goods[{goods['goods_sn']}][goods_sn]": goods['goods_sn'],
                f"package_length_{goods['goods_sn']}": goods['package_length'],
                f"package_width_{goods['goods_sn']}": goods['package_width'],
                f"package_height_{goods['goods_sn']}": goods['package_height'],
                f"goods_weight_{goods['goods_sn']}": goods['goods_weight'],
                f"goods[{goods['goods_sn']}][picking_quantity]": goods['goods_quantity'],
                "goods_weight": goods['goods_weight']
            }
            if sku:
                if sku == goods['goods_sn']:
                    picking_data.update(picking_goods_data)
                    break
            else:
                picking_data.update(picking_goods_data)
        # 请求配货
        picking_url = "http://oms.hqygou.com/order/picking/save"
        response = oms_session.session.post(picking_url, picking_data).json()
        logger.info('{}配货结果：{}'.format(self.order_sn, response))
        return response


if __name__ == '__main__':
    # process = OrderAllProcess('Z2012222036285905')
    process = OrderAllProcess('L21110301132201812')
    print(process.add_sku("65555563222,867565212"))
