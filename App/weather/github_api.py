#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : weather_request.py
# @Description:  weather_request
import requests
import json
import logging
from App.utils import success_return, error_return
from App.extensions import redis_base
from App.settings import ProdConfig
import datetime


class GithubApi:

    BASE_URL = "http://www.7timer.info/bin/"

    @staticmethod
    def api_data(**kwargs):
        url = GithubApi.BASE_URL + "api.pl"

        # 以json格式获取
        kwargs.update({"output": "json"})

        redis_key = redis_base.create_key(kwargs["lon"], kwargs["lat"], kwargs["product"])
        try:
            redis_connect = redis_base.connect_redis_by_pool()
            redis_data = redis_base.get_redis_data(redis_connect, redis_key)
        except Exception as e:
            logging.error(str(e))
            redis_connect = None
            redis_data = None

        # 有缓存
        if redis_data:
            redis_connect.close()
            return json.loads(redis_data)
        else:
            try:
                response = requests.get(url=url, params=kwargs, timeout=10)
                if response.status_code == 200:
                    data = response.json()

                    def serialize_weather(weather_data):
                        init_time = datetime.datetime.strptime(weather_data["init"], '%Y%m%d%H')
                        weather_data["init"] = init_time.strftime('%Y-%m-%d %H:%M:%S')
                        for _ in weather_data["dataseries"]:
                            _["time"] = (init_time + datetime.timedelta(hours=_["timepoint"])).strftime('%Y-%m-%d %H:%M')

                    serialize_weather(data)
                    data = success_return(data=data, msg="查询成功")
                    # 存入缓存
                    if redis_connect:
                        try:
                            redis_base.set_redis_data(redis_connect, redis_key,
                                                      json.dumps(data, ensure_ascii=False),
                                                      ex=ProdConfig.WEATHER_CACHE_SECOND)
                        except Exception as e:
                            logging.error(str(e))
                            pass
                        finally:
                            redis_connect.close()
                    return data
                else:
                    logging.info("error GithubApi - api_data:  kwargs: %s, status_code: %s" % (
                        str(kwargs), str(response.status_code)
                    ))
                    return error_return(msg="error GithubApi - api_data", code=response.status_code)
            except Exception as e:
                logging.info("error GithubApi - api_data:  kwargs: %s, error: %s" % (
                    str(kwargs), str(e)
                ))
                return error_return(msg=str(e))
