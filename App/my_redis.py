#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : my_redis.py
# @Description:  my_redis
import hashlib

import redis


class MyRedis(object):
    """
    自行redis连接
    """
    def __init__(self):
        """
        :param host:str  ip地址
        :param port:int  端口
        :param db:int  数据库
        :param password:str  密码
        """
        self.pool = None

    def connect_redis_pool(self, url):
        """
        redis-连接池-初始化
        :param url: str  # url
        :return:None
        """
        if not isinstance(url, str):
            raise ValueError("地址格式错误")
        try:
            self.pool = redis.ConnectionPool().from_url(url=url, decode_responses=True)
        except Exception as e:
            raise e

    def connect_redis_by_pool(self):
        """
        redis-connect-by-pool
        :return: redis_connect
        """
        try:
            redis_connect = redis.Redis(connection_pool=self.pool)
        except Exception as e:
            raise e
        else:
            return redis_connect

    def connect_redis_by_host(self, host=None, port=None, db=None, password=None, **kwargs):
        """
        redis-connect-by-host
        :param host:str  ip地址
        :param port:int  端口
        :param db:int  数据库
        :param password:str  密码
        :return: redis_connect
        """
        try:
            redis_connect = redis.Redis(host=host, port=port, db=db, password=password, **kwargs)
        except Exception as e:
            raise e
        else:
            return redis_connect

    def monitor_redis(self, redis_connect, channle):
        """
        redis-monitor
        :param redis_connect: function  # redis连接
        :param channle: str  # 监听的渠道
        :return:
        """
        pubsub = redis_connect.pubsub()
        pubsub.subscribe(channle)
        data = pubsub.listen()
        return data

    def set_redis_data(self, redis_connect, name, value, ex=None, px=None, nx=False, xx=False):
        """
        set-redis-key
        :param redis_connect: function  # redis连接
        :param name: str  # 键
        :param value: str  # 值
        :param ex: int  # 过期时间（秒）
        :param px: int  # 过期时间（毫秒）
        :param nx: bool  # name不存在时才能执行
        :param xx: bool  # name存在时才执行
        :return:
        """
        try:
            result = redis_connect.set(name=name, value=value, ex=ex, px=px, nx=nx, xx=xx)
        except Exception as e:
            raise e
        else:
            return result

    def get_redis_data(self, redis_connect, name):
        """
        get-redis-value
        :param redis_connect:function  # redis连接
        :param name: str  # 键
        :return:
        """
        try:
            result = redis_connect.get(name)
        except Exception as e:
            raise e
        else:
            return result

    def delete_redis_data(self, redis_connect, name):
        """
        delete-redis-value
        :param redis_connect:function  # redis连接
        :param name:str  # 键
        :return:
        """
        try:
            result = redis_connect.delete(name)
        except Exception as e:
            raise e
        else:
            return result

    def right_push_list_redis_data(self, redis_connect, list_name, *data):
        """
        right-push-list-to-data
        :param redis_connect:function  # redis连接
        :param list_name:str  # 列表名称
        :param data:
        :return:
        """
        try:
            result = redis_connect.rpush(list_name, *data)
        except Exception as e:
            raise e
        else:
            return result

    def left_push_list_redis_data(self, redis_connect, list_name, *data):
        """
        right-push-list-to-data
        :param redis_connect:function  # redis连接
        :param list_name:str  # 列表名称
        :param data:
        :return:
        """
        try:
            result = redis_connect.lpush(list_name, *data)
        except Exception as e:
            raise e
        else:
            return result

    def left_get_list_redis_data(self, redis_connect, list_name, timeout):
        """
        right-push-left_get_list_redis_data
        :param redis_connect:function  # redis连接
        :param list_name:str  # 列表名称
        :param data:
        :return:
        """
        try:
            result = redis_connect.blpop(list_name,timeout)
        except Exception as e:
            raise e
        else:
            return result

    def delete_list_redis_data(self, redis_connect, list_name, value, count=0):
        """
        delete-list-data
        :param redis_connect: function  # redis连接
        :param list_name: str  # 列表名称
        :param data:
        :return:
        """
        try:
            result = redis_connect.lrem(list_name, count, value)
        except Exception as e:
            raise e
        else:
            return result

    def hash_set_redis_data(self, redis_connect, dict_name, key, value):
        """
        set-dict-data
        :param redis_connect: function  # redis连接
        :param dict_name: str  # 列表名称
        :param key: str
        :param value: str
        :return:
        """
        try:
            result = redis_connect.hset(name=dict_name, key=key, value=value)
        except Exception as e:
            raise e
        else:
            return result

    def hash_get_redis_data(self, redis_connect, dict_name, key):
        """
        get-dict-data
        :param redis_connect: function  # redis连接
        :param dict_name: str  # 列表名称
        :param key: str
        :return:
        """
        try:
            result = redis_connect.hget(dict_name, key)
        except Exception as e:
            raise e
        else:
            return result

    def hash_delete_redis_data(self, redis_connect, dict_name, *keys):
        """
        delete-dict-data
        :param redis_connect: function  # redis连接
        :param dict_name: str  # 列表名称
        :param keys: tuple  # key
        :return:
        """
        try:
            result = redis_connect.hdel(dict_name, *keys)
        except Exception as e:
            raise e
        else:
            return result

    def get_redis_keys(self, redis_connect, pattern='*'):
        """
        get-redis-keys
        :param redis_connect: function  # redis连接
        :param pattern: 正则， 默认* 全部
        :return:
        """
        try:
            result = redis_connect.keys(pattern)  # 获取所有键
        except Exception as e:
            raise e
        else:
            return result

    def hash_get_redis_keys(self, redis_connect, dict_name):
        """
        get-dict-keys
        :param redis_connect: function  # redis连接
        :param dict_name: str  # 列表名称
        :return:
        """
        try:
            result = redis_connect.hkeys(dict_name)
        except Exception as e:
            raise e
        else:
            return result

    def hash_get_redis_all_data(self, redis_connect, dict_name):
        """
        get-dict-all-data
        :param redis_connect: function  # redis连接
        :param dict_name: str  # 列表名称
        :return:
        """
        try:
            result = redis_connect.hgetall(dict_name)
        except Exception as e:
            raise e
        else:
            return result

    def expire(self, redis_connect, name, time_out):
        """
        set-time_out
        :param redis_connect: function  # redis连接
        :param name: str  # key
        :param time_out: int  # 超时时间（秒）
        :return:
        """
        try:
            result = redis_connect.expire(name=name, time=time_out)
        except Exception as e:
            raise e
        else:
            return result

    def ttl(self, redis_connect, name):
        """
        获取有效时间
        """
        try:
            result = redis_connect.ttl(name)
        except Exception as e:
            raise e
        else:
            return result

    def flushdb(self, redis_connect):
        """
        清空数据库
        """
        try:
            result = redis_connect.flushdb()
        except Exception as e:
            raise e
        else:
            return result

    @staticmethod
    def create_key(*args):
        if not args:
            raise Exception("args is empty")
        key = "".join([str(_) for _ in args])
        return hashlib.md5(key.encode("utf-8")).hexdigest()

