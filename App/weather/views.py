#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : views.py
# @Description:  views

import logging
from flask import Blueprint, jsonify, request
import jsonschema  # 进行json的校验
from jsonschema import ValidationError
from flask_restplus import Resource
from flask_jwt_extended import jwt_required
from App.auth import option_required
from App.pubilc_response import parameter_error, weather_error
from App.extensions import api_docs
from App.weather.schema import search_schema
from App.weather.github_api import GithubApi
from App.weather.swagger import response_model

blueprint = Blueprint("weather", __name__, url_prefix="/weather")
ns = api_docs.namespace('weather', description='天气')


@ns.route('/')
class Weather(Resource):

    # 只能一个一个写？  未优化
    @ns.param("Authorization", description="token，startswith 'JWT '", _in='header', type=str, required=True,)
    @ns.param("lon", description="经度", _in='query', type=str, required=True,)
    @ns.param("lat", description="维度", _in='query', type=str, required=True,)
    @ns.param("product", description="产品", _in='query', type=str, required=True,
              enum=("astro", "civil", "civillight", "meteo"))
    @ns.response(200, "成功", response_model)
    @jwt_required
    @option_required
    def get(self):
        logging.info("天气搜索-login")

        # 验证参数
        json_data = dict(request.args)
        try:
            jsonschema.validate(json_data, search_schema)
        except ValidationError as e:
            logging.error("错误信息：%s， 请求参数: %s 。" % (e.message, str(json_data)))
            return jsonify(parameter_error)

        data = GithubApi.api_data(**json_data)
        if data["success"]:
            return jsonify(data)
        else:
            return jsonify(weather_error)

