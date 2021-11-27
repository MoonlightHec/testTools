# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/15 16:59 
# @Author : lijun7 
# @File : format.py
# @desc : 格式化各种数据
"""

import phpserialize

from app.log.mLogger import logger


class Format:
    def __init__(self, string):
        self.string = string

    def serialize(self):
        """
        PHP序列化数据,如果字符串有中文转换的Unicode会不准
        :return:
        """
        serialized = phpserialize.dumps(self.string, charset='utf-8')
        logger.info("PHP序列化前：【{}】\n序列化后：【{}】".format(self.string, serialized))
        return serialized


if __name__ == '__main__':
    shipping = '[{"outhouse":[{"order_number_new":"U2111151636942842186986280","tracking_number":"40111151636942842","transfer_no":null,"express_id":"1530","is_photo":"2","express_code":"CAEXPXH","out_warehouse_number":"XH111151636942842","weight":"1.2390","volume_weight":"0.0010","shipping_fee":"18.2980","currency_code":"USD","creator":"fujunjuan","create_time":"2021-07-17 16:07:21","qc_number":"QC62","qc_name":"Manual delivery","product_outhouse":[{"goods_sn":"148786003","out_house_quantity":"1","shipper":[{"amount":"1","prepare_shipper_no":"FZ001"}],"is_distribution":1}],"declaration":[{"goods_sn":"148786003","package_description":"hoodies","declare_name_zh":"EMS(SZ)","commodity_quantity":"1","commodity_unit_value":"3.55","customs_code":"6109100010","express_id":"1530","express_code":"CAEXPXH","single_price":"9.78133","head_cost":0,"sales_head_cost":0,"tariff":0,"value_added_tax":0,"duties":0,"other_cost":0,"currency":"USD","usd_cost_adjust":0,"rate":"1.0000000000","relevant_add_time":"2020-09-03 20:23:41"}],"logistics_code":"XHWL","logistics_name":"EMS(SZ)","picking_type":"1","order_shipper_no":"FZ001"}]}]'
