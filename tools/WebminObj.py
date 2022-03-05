# _*_ coding: utf-8 _*_
"""
# @Time : 2021/8/26 17:24 
# @Author : lijun
# @File : WebminObj.py
# @desc : webmin脚本顶级类
"""
import os

import requests
from flask import json

# 禁用安全警告信息；requests忽略ssl证书后，控制台不再输出警告信息
from tools.readconfig import ReadConfig

requests.packages.urllib3.disable_warnings()


def get_headers(app_name):
    """
    获取headers
    :param app_name:
    :return:
    """
    headers = {
        "Cookie": "testing=1; sid=x"
    }

    # 读取webmin登陆配置文件
    rc = ReadConfig("/webmin_config.ini", app_name.upper())
    url = rc.get_value("url")
    data = {
        "page": "/",
        "user": rc.get_value("user"),
        "pass": rc.get_value("password"),
        "save": 1
    }

    # 获取cookies
    res = requests.post(url=url, headers=headers, data=data, verify=False, allow_redirects=False)
    cookiejar = res.cookies
    sid = requests.utils.dict_from_cookiejar(cookiejar)['sid']
    headers['Cookie'] = 'testing=1; sid={}'.format(sid)
    return headers


class WebminObj:
    def __init__(self, app_name='oms'):

        self.headers = get_headers(app_name)
        # 获取脚本通用参数
        self.absolute_path = os.path.dirname(os.path.abspath(__file__))
        with open(f'{self.absolute_path}/resource/webmin_script_data.json', 'r', encoding='utf-8') as data_stream:
            self.data = json.load(data_stream)
        # 获取要执行的脚本参数
        with open(f'{self.absolute_path}/resource/webmin_args.json', 'r', encoding='utf8') as params_stream:
            self.request_info = json.load(params_stream)[app_name.lower()]

    def run_script(self, script_name, *args):
        try:
            params = self.request_info[script_name]
        except KeyError:
            print("脚本名不存在")
            return "脚本名不存在"
        self.headers['Referer'] = self.request_info['config']['Referer']
        self.data['idx'] = self.request_info['config']['idx']
        self.data['user'] = self.request_info['config']['user']
        save_url = self.request_info['config']['save_url']
        execute_url = self.request_info['config']['execute_url'].format(self.data['idx'])

        # 获取要执行的脚本参数
        self.data['comment'] = params['comment']
        try:
            self.data['cmd'] = params['cmd'].format(*args)
        except IndexError:
            print("参数个数错误")
            return "参数个数错误"
        # 禁止重定向，否则重定向到/cron/exec_cron.cgi后，执行会因为没有cookie导致执行脚本报权限不足
        print("\n----------------------------开始保存脚本----------------------------")
        save_res = requests.get(url=save_url, headers=self.headers, params=self.data, verify=False,
                                allow_redirects=False)
        if save_res.status_code == 302:
            print("\n----------------------------保存成功----------------------------")
            # 执行脚本
            print("\n----------------------------开始执行脚本----------------------------")
            exec_res = requests.get(url=execute_url, headers=self.headers, verify=False)
            print(exec_res.text)
            with open(f'{self.absolute_path}/resource/webmin_script_result.html', 'w', encoding='utf-8') as fd:
                fd.write(exec_res.text)
            return exec_res.text
        else:
            print("\n----------------------------脚本保存失败----------------------------")


def run_oms():
    """
    # 接收soa订单
    # 地址异常生成电联工单
    # 推送异常工单到wos
    # 退款到原支付 param：【826:WAX_CC】
    # 退款到电子钱包 param：退款申请编号
    # 推送邮件队列列表到SMS param：【ticket_receive】
    # 自动去信加入队列
    # 匹配订单
    # 同步配货单到wms
    # 接收wms发货数据

    # 联合订单:
    # 1.soa_mq_oms_received
    # 2.
    # 3.
    """
    oms_script = WebminObj(app_name='oms')
    order_sn = 'U2112240257259056'
    # oms_script.run_script('soa_mq_oms_received')
    # oms_script.run_script('推送异常工单到wos')
    oms_script.run_script('推送邮件队列列表到SMS', 'ticket_receive')


def run_sms():
    """
    # 发送邮件：send_email
    # 发送TK：auto_send_ticket
    # 生成ticket并发送：auto_generate_ticket
    # TK回复消息推送到支持中心：send_reply_support
    # 发送站内信队列：send_station_queue
    """
    sms_script = WebminObj(app_name='sms')
    order_sn = 'hgfoahwou445 '
    sms_script.run_script('send_station_queue')


def run_lms():
    """
    # 更新箱子状态
    :return:
    """
    lms_script = WebminObj(app_name='lms')
    lms_script.run_script('更新箱子状态')


def run_pms():
    """
    # 推送采购入库明细数据：push_purchase_info 时间:2022-01-31
    :return:
    """
    pms_script = WebminObj(app_name='pms')
    pms_script.run_script('push_purchase_info', '2022-2-12', '2022-02-14')


def run_fas():
    """
    # 接收采购入库明细数据：get_purchase_info
    :return:
    """
    pms_script = WebminObj(app_name='fas')
    pms_script.run_script('get_purchase_info')


if __name__ == '__main__':
    # run_pms()
    run_fas()
