# -*- coding:utf-8 -*-
# Author:      zhousf
# Date:        2018-12-21
# File:        response_info.py
# Description:  
import json


class Response(object):
    """
    网络响应信息体
    """

    def __init__(self, code=200, message='Successful connection.', data=None):
        self.code = code
        self.message = message
        if data:
            self.data = data


class Data(object):
    """
    数据信息体
    """

    def __init__(self, code, message, result):
        self.code = code
        self.message = message
        if result:
            self.result = result


def package(code, message):
    info = Response(code, message)
    return json.dumps(info.__dict__, sort_keys=True, ensure_ascii=False)


def business(code, message, result=None):
    data = Data(code, message, result)
    info = Response()
    info.data = data.__dict__
    return json.dumps(info.__dict__, sort_keys=True, ensure_ascii=False)



