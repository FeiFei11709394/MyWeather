#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : pubilc_response.py
# @Description:  pubilc_response

from App.utils import error_return, success_return

parameter_error = error_return(msg="参数错误", code=500)
not_user_error = error_return(msg="用户不存在", code=500)
pwd_error = error_return(msg="密码错误", code=500)
auth_error = error_return(msg="错误的身份信息", code=401)

weather_error = error_return(msg="查询失败，请稍后重试", code=500)
