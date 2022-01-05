# -*- coding: utf-8 -*-
# @Time : 2021/12/10 09:44
# @Author : lijun
# @File : proofing.py
# @desc :
from tools.get_session import LoginSession


class Proofing:
    """
    样品开发->打版全流程
    """

    def __init__(self):
        self.session = LoginSession(app_name='plm').session
        pass

    def sample_develop(self):
        """
        样品开发
        :return:
        """
        
