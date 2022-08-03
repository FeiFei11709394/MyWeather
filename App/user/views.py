#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : views.py
# @Description:  views

import logging
from flask import Blueprint, jsonify, request
import jsonschema  # 进行json的校验
from jsonschema import ValidationError
from flask_jwt_extended import create_access_token
from flask_restplus import Resource
from App.utils import success_return
from App.pubilc_response import parameter_error, not_user_error, pwd_error
from App.extensions import api_docs
from App.user.models import User
from App.user.schema import login_schema
from App.user.swagger import model, response_model

blueprint = Blueprint("user", __name__, url_prefix="/user")
ns = api_docs.namespace('user', description='用户')


@ns.route('/login/')
class Login(Resource):

    @ns.expect(model)  # 未使用validate功能
    @ns.response(200, "成功", response_model)
    # @ns.marshal_with(request_mode) # 强制序列化输出
    def post(self):
        """用户登录
        """
        logging.info("用户登录-login")

        # 验证参数
        json_data = request.get_json(force=True)
        try:
            jsonschema.validate(json_data, login_schema)
        except ValidationError as e:
            logging.error("错误信息：%s， 请求参数: %s 。" % (e.message, str(json_data)))
            return jsonify(parameter_error)

        user = User.query.filter_by(user_name=json_data["user_name"], status=1).first()
        if user:
            if user.check_password(json_data["password"]):

                return jsonify(success_return(
                    {"token": create_access_token(identity=user.user_name)},
                    "登录成功")
                )
            else:
                return jsonify(pwd_error)
        else:
            return jsonify(not_user_error)
