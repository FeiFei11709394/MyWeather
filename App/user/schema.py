#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : schema.py
# @Description:  schema

login_schema = {
        "type": "object",
        "properties": {
            "user_name": {"type": "string", "description": "用户名", "pattern": "^[\S]+$"},
            "password": {"type": "string", "description": "密码", "pattern": "^[\S]+$"},
        },
        "required": ["user_name", "password"]  # 必填项
    }
