#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : schema.py
# @Description:  schema


search_schema = {
        "type": "object",
        "properties": {
            "lon": {"type": "string", "description": "经度", "pattern": "^[\S]+$"},
            "lat": {"type": "string", "description": "纬度", "pattern": "^[\S]+$"},
            "product": {"type": "string", "description": "产品类型",
                        "enum": ["astro", "civil", "civillight", "meteo"]
                        },
        },
        "required": ["lon", "lat", "product"]
    }
