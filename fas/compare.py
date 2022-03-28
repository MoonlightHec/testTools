# -*- coding: utf-8 -*-
# @Time : 2022/3/7 11:16
# @Author : sakura
# @File : compare.py
# @desc : 一本帐数据对比
from decimal import Decimal

from tools.DB import DB


def compare(actual, expect):
    if not actual:
        return
    miss_list = []
    for key, value in actual.items():
        try:
            if value == expect[key]:
                print("{}:【actual:{},expect:{}】".format(key, value, expect[key]))
            else:
                print('\033[31;1m{}:【actual:{},expect:{}】 \033[0m'.format(key, value, expect[key]))
        except KeyError:
            miss_list.append(key)
    print("\n缺少的数据：{}".format(miss_list))


class ResourceDataDraw:
    """
    源数据提取汇总初稿
    """

    def __init__(self, table='source_voucher_202203', unique_source_code='', cert_type=None):
        self.db = DB('fas')
        self.cert_type = cert_type
        sql = "select * from %s where unique_source_code ='%s';"
        source_data = self.db.query(sql, table, unique_source_code)[0]
        self.type_code = source_data.get('type_code')
        self.data = eval(source_data.get('data'))
        self.source_id = source_data.get('snowflake_id')

    def get_compare(self):
        com_type = {
            '0301': self.income_sale
        }
        try:
            actual, expect = com_type.get(self.type_code)()
        except TypeError:
            return
        compare(actual, expect)

    def get_actual_data(self, table):
        actual_data_sql = "select * from %s where source_id='%s' and certificate_type_two='%s';"
        try:
            return self.db.query(actual_data_sql, table, self.source_id, self.cert_type)[0]
        except IndexError:
            print("源数据还未提取")

    def income_sale(self):
        """
        收入凭证提取
        """
        # 实际结果
        actual_data = self.get_actual_data('income_summary_voucher_draft')

        # 预期结果
        expect_data = {
            'source_id': self.source_id,
            'certificate_type_one': 6,
            'certificate_type_two': self.cert_type
        }
        # 订单数据
        order_sql = "select * from source_voucher_order where order_sn='%s';"
        try:
            order_data = self.db.query(order_sql, self.data.get('order_sn'))[0]
            # 交易类型
            if order_data.get('customer_id') in [187489462, 188160872, 188213033]:
                expect_data['trade_type'] = 1
            elif order_data.get('settlement') == 2 and order_data.get('customer_company') == '深圳市希航国际货运代理有限公司':
                expect_data['trade_type'] = 2
            elif order_data.get('order_type_id') == 5:
                expect_data['trade_type'] = 3
            else:
                expect_data['trade_type'] = 4
        except TypeError:
            print("订单数据不存在")
            expect_data['trade_type'] = 4

        # 下单时间
        sale_date = self.data['sale_time']
        sale_date_year = int(sale_date[:4])
        # 法人简称
        corporate_code_switcher = {
            'XSPT0006': 'HKDAISLEY' if sale_date_year >= 2022 else 'SOUTHSTAR1',  # DL
            'XSPT0008': 'HKBIAN' if sale_date_year >= 2022 else 'SOUTHSTAR1',  # RG
            'XSPT0098': 'SZSFSY'
        }
        try:
            expect_data['corporate_code'] = corporate_code_switcher[self.data['order_from']]
        except KeyError:
            # 网站来源为空时，根据事业部取法人
            department = {
                'SYB0036': 'HKBIAN',
                'SYB0037': 'HKDAISLEY',
            }
            corporate_code = ''
            if self.data['order_from'] is None or self.data['order_from'] == '':
                corporate_code = department.get(self.data['department_sn'])
            expect_data['corporate_code'] = corporate_code if corporate_code else 'SOUTHSTAR1'

        expect_data['department_sn'] = self.data.get('department_sn')
        expect_data['order_from'] = self.data.get('order_from')
        statistics_day = self.data.get('ensure_time')
        expect_data['statistics_day'] = statistics_day.split(' ')[0].replace('-', '')
        amount = self.data.get('purchase_cost') if self.cert_type == 17 else float(
            self.data.get('product_total')) + float(self.data.get('other_income'))
        expect_data['amount'] = Decimal(amount).quantize(Decimal('0.00000'))
        expect_data['currency_code'] = 'USD'
        expect_data['corporate_currency_rate'] = self.get_currency_rate('USD', expect_data.get('corporate_code'),
                                                                        statistics_day[:7].replace('-', ''))
        return actual_data, expect_data

    def get_currency_rate(self, ori_currency_code, corporate_code, time):
        """
        查询汇率
        """
        currency_tag = {
            'USD': 'usd_rate',
            'CNY': 'cny_rate',
            'HKD': 'hkd_rate'
        }
        # 汇率数据
        db = DB('fas1')
        rate_sql = "select * from fas1.c_currency_rate where currency='%s' and the_month_cd='%s';"
        try:
            currency_rate = db.query(rate_sql, ori_currency_code, time)[0]
        except IndexError:
            return 0
        # 获取法人核算币种
        corporate_sql = "select * from b_corporate_info where corporate_code='%s';"
        corporate_info = self.db.query(corporate_sql, corporate_code)[0]
        return Decimal(currency_rate.get(currency_tag[corporate_info.get('use_currency')])).quantize(
            Decimal('0.0000000000'))


if __name__ == '__main__':
    res = ResourceDataDraw(unique_source_code='627354811_1', cert_type=16)
    res.get_compare()
