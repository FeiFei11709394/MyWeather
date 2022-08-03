#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : utils.py
# @Description:  utils


def success_return(data=None, msg="", **kwargs):
    """
    正常响应的返回
    :param data: 需要返回的数据
    :param msg: 文字信息
    :param kwargs: 其他需要返回的字段
    :return:
    """
    res = {
        "success": True,
        "data": data,  # 数据
        "msg": msg,  # 信息
        "code": 200,  # 响应码
    }
    if kwargs:
        for key, value in kwargs.items():
            res[key] = value
    return res


def error_return(msg="", code=87014):
    """
    错误信息的返回
    :param data: 错误数据
    :param msg: 文字信息
    :param code: 错误代码
    :return:
    """
    return {
        "success": False,
        "data": None,  # 数据
        "msg": msg,  # 信息
        "code": code,  # 响应码
    }


