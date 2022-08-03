#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : app.py
# @Description:  app

import logging
import json
from flask import Flask, request, make_response, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix

from App.settings import ProdConfig
from App.extensions import cors, db, logcfg, migrate, jwt, security, api_docs, scheduler
from App.utils import error_return
from App import user, weather
import atexit
import platform

def create_app(config_object=ProdConfig):
    """创建flask实例
    """
    app = Flask(__name__.split(".")[0])

    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.config.from_object(config_object)

    @app.after_request
    def add_header(response):
        response.headers["X-SaintIC-Media-Type"] = "saintic.v1"
        response.headers["Access-Control-Allow-Origin"] = "*"
        # 记录详细信息
        logging.info(json.dumps({
            "AccessLog": {
                "method": request.method,  # 请求方式
                "remote ip": request.headers.get('X-Real-Ip', request.remote_addr),  # 请求ip地址
                "referer": request.headers.get('Referer'),  # 请求来源 url
                "agent": request.headers.get("User-Agent"),  # 请求的浏览器信息
                "url": request.url,  # 请求本系统的那个url
                "status_code": response.status_code,  # 响应结果
            }
        }
        ))
        return response

    register_blueprints(app)
    register_extensions(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    """初始化插件
    """
    cors.init_app(app, supports_credentials=True)
    with app.app_context():
        db.init_app(app)
        # 表映射到数据库
        db.create_all()
    jwt.init_app(app)
    security.init_app(app)
    logcfg.init_app(app)
    migrate.init_app(app, db)
    api_docs.init_app(app, **ProdConfig.SWAGGER_INFO)
    scheduler_init(app)


def register_blueprints(app):
    """注册蓝图"""
    app.register_blueprint(user.views.blueprint)  # 录波数据
    app.register_blueprint(weather.views.blueprint)  # 录波数据


def register_errorhandlers(app):
    """Register error handlers."""
    '''
    这个是导出html，修改成返回json
    def render_error(error):
        """Render error templates."""
        # If a HTTPValidationError, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    '''
    def render_error(error):
        '''
        修改成返回错误信息
        :param error:
        :return:
        '''
        error_code = getattr(error, 'code', 500)
        error_message = {
            400: "错误请求，如语法错误",
            401: "未授权,登录失败",
            403: "禁止访问",
            404: "没有发现文件、查询或URl",
            500: "内部服务器错误",
        }
        return make_response(jsonify(
            error_return(msg=error_message[error_code],
                         code=error_code
                         )
        ), error_code)

    for errcode in [400, 401, 403, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def scheduler_init(app):
    """
    保证系统只启动一次定时任务
    :param app:
    :return:
    """
    if platform.system() != 'Windows':
        fcntl = __import__("fcntl")
        f = open('scheduler.lock', 'wb')
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            scheduler.init_app(app)
            scheduler.start()
            app.logger.debug('Scheduler Started,---------------')
        except:
            pass

        def unlock():
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()

        atexit.register(unlock)
    else:
        msvcrt = __import__('msvcrt')
        f = open('scheduler.lock', 'wb')
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            scheduler.init_app(app)
            scheduler.start()
            app.logger.debug('Scheduler Started,----------------')
        except:
            pass

        def _unlock_file():
            try:
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            except:
                pass

        atexit.register(_unlock_file)

