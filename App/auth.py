#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : auth.py
# @Description:  auth
import logging
from functools import wraps

from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from App.pubilc_response import auth_error


def option_required(f):
    """
    接口权限验证装饰器
    :param f:
    :return:
    """
    return option_permission_required()(f)


def option_permission_required():
    """
    验证权限
    """
    logging.info('permission_required')

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 解析出合法的用户名
            user_name = get_jwt_identity()
            # 检查用户名是否在数据库
            from App.user.models import User
            if not User.query.filter_by(user_name=user_name, status=1).one():
                return jsonify(auth_error)

            return f(*args, **kwargs)
        return decorated_function

    return decorator
