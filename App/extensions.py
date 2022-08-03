#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : extensions.py
# @Description:  插件实例

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_logconfig import LogConfig
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_security import Security
from flask_restplus import Api

from flask_apscheduler import APScheduler
from App.my_redis import MyRedis
from App.settings import ProdConfig

logcfg = LogConfig()  # 日志
jwt = JWTManager()  # jwt token
security = Security()  # 权限控制

cors = CORS()  # 跨域处理
db = SQLAlchemy()  # 数据库
migrate = Migrate()
api_docs = Api()  # 文档
scheduler = APScheduler()  # 定时任务

# redis
redis_base = MyRedis()
redis_base.connect_redis_pool(ProdConfig.REDIS_CONFIG)


