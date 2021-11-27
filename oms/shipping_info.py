# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/16 17:36 
# @Author : lijun7 
# @File : shipping_info.py
# @desc : OMS变更发货状态
"""
import pika

from tools.DbTools import DbTools
from tools.format import Format
from tools.myRabbitMQ import RabbitMQ

if __name__ == '__main__':
    order_sn = 'U2111171637129703'
    # 查询配货单号
    sql = "SELECT order_number_new FROM o_oms_order_picking_info WHERE order_sn ='%s';"
    db = DbTools('OMS')
    order_number_new = db.execute_sql(sql, order_sn)[0][0]
    del db
    # php序列化
    shipping_info = '[{"outhouse":[{' \
                    f'"order_number_new":"{order_number_new}",' \
                    f'"tracking_number":"40{order_sn[2:]}",' \
                    '"transfer_no":null,"express_id":"1530","is_photo":"2","express_code":"CAEXPXH",' \
                    f'"out_warehouse_number":"XH{order_sn[2:]}",' \
                    '"weight":"1.2390","volume_weight":"0.0010","shipping_fee":"18.2980","currency_code":"USD","creator":"fujunjuan","create_time":"2021-07-17 16:07:21",' \
                    '"qc_number":"QC62","qc_name":"Manual delivery","product_outhouse":[{"goods_sn":"148786003","out_house_quantity":"1","shipper":[{"amount":"1",' \
                    '"prepare_shipper_no":"FZ001"}],"is_distribution":1}],"declaration":[{"goods_sn":"148786003","package_description":"hoodies","declare_name_zh":"EMS(SZ)",' \
                    '"commodity_quantity":"1","commodity_unit_value":"3.55","customs_code":"6109100010","express_id":"1530","express_code":"CAEXPXH","single_price":"9.78133",' \
                    '"head_cost":0,"sales_head_cost":0,"tariff":0,"value_added_tax":0,"duties":0,"other_cost":0,"currency":"USD","usd_cost_adjust":0,"rate":"1.0000000000",' \
                    '"relevant_add_time":"2020-09-03 20:23:41"}],"logistics_code":"XHWL","logistics_name":"EMS(SZ)","picking_type":"1","order_shipper_no":"FZ001"}]}]'
    shipping_format = Format(shipping_info)
    message = shipping_format.serialize()

    """
    # 推送到MQ
    connection = RabbitMQ('oms').get_connection()
    # 创建一个 AMQP 信道（Channel）
    channel = connection.channel()
    # 声明消息队列orderInfo_OMS，消息将在这个队列传递，如不存在，则创建
    channel.queue_declare(queue='orderInfo_OMS')
    # 向队列插入数值 routing_key的队列名为orderInfo_OMS，body 就是放入的消息内容，exchange指定消息在哪个队列传递，这里是空的exchange但仍然能够发送消息到队列中，因为我们使用的是我们定义的空字符串“”exchange（默认的exchange）
    channel.basic_publish(exchange='', routing_key='shippingInfo_OMS', body=message)
    # 关闭连接
    connection.close()
    """
