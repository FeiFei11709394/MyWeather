#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : settings_qa.py
# @Description:  settings_qa

import os
import datetime
from urllib import parse


class Config(object):
    """基础配置"""

    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # 项目目录
    SECRET_KEY = os.environ.get('SECRET', 'xxxxxxxxxxxxxxxxxxx')
    # 密码加密存储
    SECURITY_HASHING_SCHEMES = ['pbkdf2_sha512']
    # 用于创建和验证tokens的不推荐的算法列表. 默认为 hex_md5
    SECURITY_DEPRECATED_HASHING_SCHEMES = []
    SECURITY_PASSWORD_SALT = 'xxxx2'

    JWT_BLACKLIST_ENABLED = False
    JWT_HEADER_TYPE = 'JWT'  # token添加前缀
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=30)  # 30分钟有效

    # 日志输出文件
    # LOG_FILE = './logs/{0}-{1}.logging'.format('App', datetime.datetime.now().strftime("%Y-%m-%d"))
    # 日志配置
    LOGCONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'App.my_logging.log.RequestFilter'
            }
        },
        'formatters': {
            'simple': {
                'format': '[%(asctime)s][%(pathname)s][%(filename)s:%(lineno)d] [%(funcName)s][%(levelname)s] - %(message)s'

            },
            'verbose': {
                'format': '[%(asctime)s][%(pathname)s][%(filename)s:%(lineno)d][%(funcName)s][%(levelname)s] - %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',  # TODO
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            # 'file': {
            #     'level': 'DEBUG',  # TODO
            #     'class': 'logging.FileHandler',
            #     'formatter': 'verbose',
            #     'filename': LOG_FILE,
            #     'mode': 'a',
            #     'encoding': "utf-8"
            # },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }

    # 本机sqlalchemy的配置参数
    THIS_MYSQL_USER = "root"
    THIS_MYSQL_PWD = "123456"
    THIS_MYSQL_HOST = "127.0.0.1"
    THIS_MYSQL_PORT = "3306"
    THIS_MYSQL_DB = "weather"

    # "mysql://账号:%s@IP地址:端口/数据库名称"%(parse.quote_plus(密码))
    THIS_MYSQL_STR = "mysql://%s:%s@%s:%s/" % (THIS_MYSQL_USER,
                                               parse.quote_plus(THIS_MYSQL_PWD),
                                               THIS_MYSQL_HOST,
                                               THIS_MYSQL_PORT
                                               )

    SQLALCHEMY_DATABASE_URI = THIS_MYSQL_STR + ("%s?charset=utf8mb4" % THIS_MYSQL_DB)

    SWAGGER_INFO = {
        "title": "API-1.0",
        "description": "swagger开发文档",
        "terms_url": "https://www.baidu.com",
        "contact": "Feifei-Chen",
        "contact_url": "https://www.baidu.com",
        "contact_email": "feifei18329@126.com",
        "license": "flask-restplus案例",
        "license_url": "https://github.com/noirbizarre/flask-restplus/tree/master/examples"
    }

    # 定时任务配置
    JOBS = [
        # 每整点清空缓存
        {
            'id': 'clear_redis',
            'func': 'App.task:clear_redis_func',
            'args': (),
            'trigger': 'cron',
            'hour': "*/1",
            'minute': 0,
        }
    ]
    # 线程池配置
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 3
    }
    # 调度器开关
    SCHEDULER_API_ENABLED = True

    # 直接使用redis
    REDIS_HOST = '127.0.0.1'  # ip
    REDIS_POST = 6379  # 端口
    REDIS_DB = 0  # 数据库
    REDIS_URL = 'redis://{host}:{post}/'.format(host=REDIS_HOST, post=REDIS_POST)
    REDIS_CONFIG = "{redis_base_url}{db}".format(redis_base_url=REDIS_URL, db=REDIS_DB)


class ProdConfig(Config):
    """经常变更的类"""

    # 自动打印sql语句
    SQLALCHEMY_ECHO = False
    DEBUG = False
    # 设置sqlalchemy是否自动跟踪数据库  True 请求结束自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WEATHER_CACHE_SECOND = 60 * 60  # 查询天气数据缓存时间 1小时
