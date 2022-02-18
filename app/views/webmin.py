# -*- coding: utf-8 -*-
# @Time : 2022/2/16 21:18
# @Author : sakura
# @File : webmin.py
# @desc :
from flask import Blueprint, render_template, request

from app.log.mLogger import logger
from tools.WebminObj import WebminObj

webmin = Blueprint(
    'webmin',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@webmin.route('/webmin_oms')
def webmin_oms():
    """
    oms webmin页面
    :return:
    """
    return render_template('webmin_oms.html')


@webmin.route('/webmin_pms')
def webmin_pms():
    """
    pms webmin页面
    :return:
    """
    return render_template('webmin_pms.html')


@webmin.route('/webmin_fas')
def webmin_fas():
    """
    fas webmin页面
    :return:
    """
    return render_template('webmin_fas.html')


@webmin.route('/submit', methods=['POST'])
def submit():
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
    web_script = WebminObj(app_name=request.args['sys'])
    return web_script.run_script(*webmin_params)
