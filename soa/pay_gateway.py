# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/10 15:37 
# @Author : lijun7 
# @File : pay_gateway.py
# @desc :
"""

from tools.DbTools import DbTools


class PayGateway:
    def __init__(self):
        pass

    def real_select(self, select_field, where_field):
        db = DbTools('SOA')
        pay_gateway_list = []
        # 获取sql查询语句及where条件
        for index in range(1, 65):
            table_num = 'pay_gateway_' + str(index)
            sql = "select %s from %s where %s='%s';"
            db.cursor.execute(sql % (','.join(select_field), table_num, where_field['field'], where_field['value']))
            if db.cursor.rowcount:
                print("支付状态pay_status(0-未支付 1-处理中 2-已支付 3-退款中 4-退款成功 5退款失败 6支付失败 7部分退款)")
                print("所在表：%s" % table_num)
                print('共查找出', db.cursor.rowcount, '条数据')
                for row in db.cursor.fetchall():
                    data = zip(select_field, row)
                    pay_gateway_list.append(dict(data))
        del db
        return pay_gateway_list


if __name__ == '__main__':
    pay = PayGateway()
    select_field_list = ['id', 'parent_order_sn', 'pay_sn', 'site_code', 'pay_status', 'channel_code', 'transaction_id','3ds_status']
    sql_field = {
        'field': 'parent_order_sn',
        'value': 'U2111260125292421'
    }
    pay_infos = pay.real_select(select_field=select_field_list, where_field=sql_field)
    print('--------------------------------------------')
    for pay_info in pay_infos:
        print(pay_info)
