#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : login_test.py
# @Description:  login_test
import pytest
import requests
import json


def read_json():
   return json.load(open('login.json', 'r', encoding="utf-8"))['item']


@pytest.mark.parametrize('data',read_json())
def test_json_login(data):
   r = requests.post(
       url=data['request']['url'],
       json=data['request']['body'])

   assert r.status_code == 200
   assert r.json()["code"] == data['response']["status_code"]
   assert r.json()["msg"] == data['response']["msg"]


if __name__ == '__main__':
   pytest.main(["-s", "-v", "login_test.py"])
