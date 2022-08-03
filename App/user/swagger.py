#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : swagger.py
# @Description:  swagger
from flask_restplus import fields
from App.extensions import api_docs

model = api_docs.model('Login', {
    'user_name': fields.String(title="用户名", example="root", required=True, max_length=10, min_length=4),
    'password': fields.String(title="密码", example="123456", required=True, max_length=10, min_length=6)
})


token_model = api_docs.model('Token', {
    'token': fields.String(title="token", required=True)
})

response_model = api_docs.model('Success', {
    'code': fields.Integer(title="编码", example="200", required=True),
    'success': fields.Boolean(title="状态", example="true", required=True),
    'data': fields.Nested(token_model),
    'msg': fields.String(title="文字信息", example="成功", required=True)
})