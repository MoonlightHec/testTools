# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/10 15:37 
# @Author : lijun
# @File : pay_gateway.py
# @desc :
"""
from tools.DB import DB


class PayGateway:
    @staticmethod
    def real_query(select_field, where_field):
        gateway_list = ['pay_gateway_' + str(index) for index in range(1, 65)]
        sql = "select %s from %s where %s='%s';"
        with DB('soa') as db:
            for gateway in gateway_list:
                order_infos = db.query(
                    sql % (','.join(select_field), gateway, where_field['field'], where_field['value']))
                if order_infos:
                    print("支付状态pay_status(0-未支付 1-处理中 2-已支付 3-退款中 4-退款成功 5退款失败 6支付失败 7部分退款)")
                    print("所在表：%s" % gateway)
                    print('共查找出', len(order_infos), '条数据')
                    print('--------------------------------------------')
                    return order_infos


if __name__ == '__main__':
    select_field_list = ['id', 'parent_order_sn', 'pay_sn', 'site_code', 'pay_status', 'channel_code', 'transaction_id',
                         '3ds_status']
    sql_field = {
        'field': 'parent_order_sn',
        'value': 'UUA2201042058589082'
    }
    for order in PayGateway.real_query(select_field=select_field_list, where_field=sql_field):
        print(order)
