#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : swagger.py
# @Description:  swagger
from flask_restplus import fields
from App.extensions import api_docs

wind10m_fields = api_docs.model('Wind10m', {
    'direction': fields.String(title="10m 風"),
    'speed': fields.Integer(title="未知"),
})

sign_weather_fields = api_docs.model('SignWeather', {
    'cloudcover': fields.Integer(title="云层"),
    'lifted_index': fields.Integer(title="提升指數"),
    'prec_type': fields.String(title="未知", required=True),
    'rh2m': fields.Integer(title="2m 相對濕度", required=True),
    'seeing': fields.Integer(title="能见度", required=True),
    'temp2m': fields.Integer(title="2m 溫度", required=True),
    'timepoint': fields.Integer(title="多少个小时后", required=True),
    'transparency': fields.Integer(title="大氣透明度", required=True),
    'wind10m': fields.Nested(wind10m_fields),
})

weather_fields = api_docs.model('Weather', {
    'dataseries': fields.List(fields.Nested(sign_weather_fields)),
    'init': fields.String(title="时间"),
    'product': fields.String(title="产品", required=True),
})

response_model = api_docs.model('WeatherSuccess', {
    'code': fields.Integer(title="编码", example="200", required=True),
    'success': fields.Boolean(title="状态", example="true", required=True),
    'data': fields.Nested(weather_fields),
    'msg': fields.String(title="文字信息", example="成功", required=True)
})

