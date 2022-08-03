#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : task.py
# @Description:  task
import logging
import time
from App.extensions import redis_base


def clear_redis_func():
    """清空数据库"""
    # 尝试三次
    redis_connect = None
    for _ in range(3, 6):
        try:
            redis_connect = redis_base.connect_redis_by_pool()
            redis_base.flushdb(redis_connect)
            print("clear_redis_func_ do")
        except Exception as e:
            logging.error(str(e))
            if redis_connect and getattr(redis_connect, "close"):
                redis_connect.close()

            if _ == 5:
                break
            # redis问题 等待几秒
            time.sleep(_)
            continue
        else:
            redis_connect.close()
            break
