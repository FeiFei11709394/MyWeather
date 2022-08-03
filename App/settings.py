#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : settings.py
# @Description:  settings


import os
import sys

python_env = os.environ.get('PROFILE')
print('settings.py:', python_env)

if python_env == 'qa':
    from .settings_qa import *
else:
    from .settings_dev import *