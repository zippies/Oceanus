# -*- coding: utf-8 -*-
from datetime import datetime
from flask_login import UserMixin
from mock_server import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


login_manager.session_protection = "strong"
login_manager.login_view = "mock-server.login"
login_manager.login_message = {"type":"error","message":"请登录后使用该功能"}


class User(db.Model, UserMixin):
    # __tablename__ = "suihouzhu_mockserver_user"

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(32))
    ip = db.Column(db.String(64))
    createdtime = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, nickname, ip):
        self.nickname = nickname
        self.ip = ip

    def __repr__(self):
        return "<User:%s>" % self.nickname


class Api(db.Model):

    # __tablename__ = "suihouzhu_mockserver_api"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(128))
    method = db.Column(db.String(64))
    httpcode= db.Column(db.Integer)
    resp_type = db.Column(db.String(32))
    resp_default = db.Column(db.Text)
    status = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer)
    created_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, path, method, httpcode, resp_type, resp_default, user_id):
        self.path = path
        self.method = method
        self.httpcode = httpcode
        self.resp_type = resp_type
        self.resp_default = resp_default
        self.user_id = user_id

    def to_json(self):
        return {
            "id": self.id,
            "path": self.path,
            "method": self.method,
            "httpcode": self.httpcode,
            "resp_type": self.resp_type,
            "resp_default": self.resp_default,
            "create_user": User.query.filter_by(id=self.user_id).first().nickname if self.user_id !=0 else "remote",
            "created_time": self.created_time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __repr__(self):
        return "<Config id='%s' path='%s'>" % (self.id, self.path)


class Condition(db.Model):

    # __tablename__ = "suihouzhu_mockserver_condition"

    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer)
    condition = db.Column(db.String(32))
    operation = db.Column(db.String(32))
    value = db.Column(db.String(128))
    httpcode= db.Column(db.Integer)
    resp_body = db.Column(db.Text)
    status = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer)
    created_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, api_id, condition, operation, value, httpcode, resp_body, user_id):
        self.api_id = api_id
        self.condition = condition
        self.operation = operation
        self.value = value
        self.httpcode = httpcode
        self.resp_body = resp_body
        self.user_id = user_id

    def to_json(self):
        return {
            "id": self.id,
            "api_id": self.api_id,
            "condition": self.condition,
            "operation": self.operation,
            "value": self.value,
            "httpcode": self.httpcode,
            "resp_body": self.resp_body,
            "create_user": User.query.filter_by(id=self.user_id).first().nickname if self.user_id != 0 else "remote",
            "created_time": self.created_time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __repr__(self):
        return "<Condition id='%s' api_id='%s'>" % (self.id, self.api_id)


class Advice(db.Model):

    # __tablename__ = "suihouzhu_mockserver_advice"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer)
    created_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

