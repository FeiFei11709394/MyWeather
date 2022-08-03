#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : models.py
# @Description:  models
from App.extensions import db
import datetime
from flask_security import UserMixin
from flask_security.utils import hash_password, verify_password


class User(UserMixin, db.Model):
    """用户表"""
    __tablename__ = "user"

    user_name = db.Column(db.String(10), comment="用户名", primary_key=True)
    password = db.Column(db.String(255), comment="密码", nullable=False)
    admin = db.Column(db.SmallInteger, comment="是否管理员", nullable=False, default=0)  # 1 是 ，0 否
    nick_name = db.Column(db.String(10), comment="昵称", nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment="生成时间")
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, comment="更新时间")
    status = db.Column(db.SmallInteger, comment="状态", nullable=False, default=1)  # 1 正常 ，0 删除

    @property
    def _password(self):
        return self.password

    @_password.setter
    def _password(self, password):
        self.password = hash_password(password)

    def check_password(self, password):
        return verify_password(password, self.password)

    def __repr__(self):
        return "<user> - %s: %s" % (self.user_name, self.nick_name)

