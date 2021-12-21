# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/30 16:01 
# @Author : lijun7 
# @File : oms.py
# @desc :
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.config import host_url
from app.log.mLogger import logger
from app.server.tools_oms import create_oms_order
from oms.order_all_process import OrderAllProcess
from tools.WebminObj import WebminObj

oms = Blueprint(
    'oms',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@oms.route('/oms_create_order', methods=['GET', 'POST'])
def oms_create_order():
    """
    系统主页/OMS首页
    :return:
    """
    return render_template('oms_create_order.html', host=host_url)


@oms.route('/oms_webmin', methods=['GET', 'POST'])
def oms_webmin():
    """
    oms webmin脚本页面
    :return:
    """
    return render_template('oms_webmin.html', host=host_url)


@oms.route('/oms_process', methods=['GET', 'POST'])
def oms_process():
    """
    oms 订单全流程页面
    :return:
    """
    return render_template('oms_process.html', host=host_url)


@oms.route('/oms_process/<path:order_sn>', methods=['GET', 'POST'])
def get_order_redirect(order_sn):
    """
    重定向到订单全流程页面
    :param order_sn:
    :return:
    """
    return render_template('oms_process.html', host=host_url, order_sn=order_sn)


@oms.route("/create_order", methods=["GET", "POST"])
def get_order_info():
    """
    oms创建订单
    :return:
    """
    print("header {}".format(request.headers))
    print("args ", request.args)
    logger.info("form表单数据 {}".format(request.form.to_dict()))
    # 将获取到的表单数据转化为dict
    user_order_info = request.form.to_dict()
    order_sn = create_oms_order(user_order_info)
    if order_sn:
        logger.info("OMS创建订单成功：{}".format(order_sn))
        flash("创建订单成功")
        return redirect(url_for('oms.get_order_redirect', order_sn=order_sn))
        # return render_template()
    return "创建失败"


@oms.route('/webmin', methods=['GET', 'POST'])
def run_webmin():
    """
    执行webmin脚本
    :return:
    """
    script_info = request.form.to_dict()
    logger.info("执行webmin脚本：form表单数据 {}".format(script_info))
    webmin_params = []
    for value in script_info.values():
        if value:
            webmin_params.append(value)
    web_script = WebminObj(app_name='oms')
    return web_script.run_script(*webmin_params)


@oms.route('/allProcess/addSkuOms', methods=['GET', 'POST'])
def add_sku_oms():
    """
    添加sku到oms产品库
    :return:
    """
    sku_list = request.form.to_dict()
    logger.info("要添加到oms的sku:form表单数据 {}".format(sku_list))
    if sku_list['sku-list']:
        process = OrderAllProcess('')
        flash(process.add_sku(sku_list['sku-list']))
        return redirect(url_for('oms.oms_process'))
    flash("请输入sku")
    return redirect(url_for('oms.oms_process'))


@oms.route('/allProcess/orderFromSite', methods=['GET', 'POST'])
def site_push_order():
    """
    网站推送订单到oms
    :return:
    """
    order_info_site = request.form.to_dict()
    logger.info("网站推送订单到oms:form表单数据 {}".format(order_info_site))
    if order_info_site['order-sn']:
        process = OrderAllProcess(order_info_site['order-sn'])
        flash(process.site_push_order(order_info_site['order-from']))
        return redirect(url_for('oms.get_order_redirect', order_sn=order_info_site['order-sn']))
    flash("请输入订单号")
    return redirect(url_for('oms.oms_process'))


@oms.route('/allProcess/receive_order', methods=['GET', 'POST'])
def oms_receive_order():
    """
    oms接收订单webmin脚本
    :return:
    """
    script_info = request.form.to_dict()
    logger.info("oms接收网站订单webmin脚本：form表单数据 {}".format(script_info))
    webmin_params = ["接收soa订单"]
    for value in script_info.values():
        if value:
            webmin_params.append(value)
    web_script = WebminObj(app_name='oms')
    return web_script.run_script(*webmin_params)


@oms.route('/allProcess/payOrderAudit', methods=["GET", "POST"])
def order_process_audit_payorder():
    """
    审核付款单
    :return:
    """
    order_sn_web = request.form.to_dict()
    logger.info("oms审核付款单:form表单数据 {}".format(order_sn_web))
    if order_sn_web['order-sn']:
        process = OrderAllProcess(order_sn_web['order-sn'])
        flash(process.audit_payorder())
        return redirect(url_for('oms.get_order_redirect', order_sn=order_sn_web['order-sn']))
    flash("请输入订单号")
    return redirect(url_for('oms.oms_process'))


@oms.route("/allProcess/dealQuestion", methods=["GET", "POST"])
def order_process_deal_question():
    """
    oms处理订单问题
    :return:
    """
    order_sn_web = request.form.to_dict()
    logger.info("oms处理订单问题:form表单数据 {}".format(order_sn_web))
    if order_sn_web['order-sn']:
        process = OrderAllProcess(order_sn_web['order-sn'])
        flash(process.deal_question())
        return redirect(url_for('oms.get_order_redirect', order_sn=order_sn_web['order-sn']))
    flash("请输入订单号")
    return redirect(url_for('oms.oms_process'))


@oms.route("/allProcess/createPickingOrder", methods=["GET", "POST"])
def order_process_picking_order():
    """
    oms生成配货单
    :return:
    """
    picking_info = request.form.to_dict()
    logger.info("oms生成配货单:form表单数据 {}".format(picking_info))
    if picking_info['order-sn']:
        process = OrderAllProcess(picking_info['order-sn'])
        flash(process.oms_piking_order(sku=picking_info['goods-sn'], stock_id=picking_info['stock-id'], express_id=picking_info['express-id']))
        return redirect(url_for('oms.get_order_redirect', order_sn=picking_info['order-sn']))
    flash("请输入订单号")
    return redirect(url_for('oms.oms_process'))


@oms.route("/allProcess/postPickingInfo", methods=["GET", "POST"])
def order_process_post_picking():
    """
    oms同步配货单
    :return:
    """
    order_sn_web = request.form.to_dict()
    logger.info("oms同步配货单:form表单数据 {}".format(order_sn_web))
    if order_sn_web['order-sn']:
        process = OrderAllProcess(order_sn_web['order-sn'])
        web_script = WebminObj(app_name='oms')
        return web_script.run_script('同步配货单到WMS', process.get_picking_sn())
    return "请输入订单号"


@oms.route("/allProcess/getPickingInfo", methods=["GET", "POST"])
def order_process_get_picking():
    """
    wms接收配货单生成包裹
    :return:
    """
    order_sn_web = request.form.to_dict()
    logger.info("wms接收配货单生成包裹:form表单数据 {}".format(order_sn_web))
    if order_sn_web['order-sn']:
        process = OrderAllProcess(order_sn_web['order-sn'])
        return process.wms_get_picking_order()
    return "请输入订单号"
