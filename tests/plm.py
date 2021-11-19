# _*_ coding: utf-8 _*_
"""
# @Time : 2021/11/16 17:55 
# @Author : lijun7 
# @File : plm.py
# @desc :
"""
import requests

if __name__ == '__main__':
    url = 'http://plm.hqygou.com:8088/fabric/complete/query'
    headers = {
        "PLM-TOKEN": "30747237757B48918942994E31B96D8C"
    }
    data = {
        "offset": 1,
        "limit": 20,
        "condition": {
            "fabricApplyNumber": "",
            "fabricBigTypeCode": "",
            "fabricName": "",
            "fabricYearCode": "",
            "fabricQuarterCode": "",
            "createDate": "",
            "dealStatus": "",
            "status": "",
            "startDate": "",
            "createUser": "",
            "fabricDeveloper": "李翠华"
        }
    }
    res = requests.post(url=url, headers=headers, json=data)
