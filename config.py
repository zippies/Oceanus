# -*- encoding:utf-8 -*-
import os

env = os.getenv("ENV")

cache_timeout = 3000
cur_dir = os.path.abspath(os.path.dirname(__file__))


def get_db_url():
    if "online" in env:
        return "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db', 'data.sqlite')

    return "mysql+pymysql://user:passwd@host:port/db?charset=utf8"


def get_gitlab_key():
    if env == "k2_test":
        return ("", "")
    elif env == "k2_online":
        return ("", "")
    else:
        return ("", "")


def get_redis_key():
    if env == "k2_online":
        return "host", 6379
    elif env == "local":
        return "127.0.0.1", 6379
    else:
        return "host", 6379


class Config(object):
    SQLALCHEMY_DATABASE_URI = get_db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_RECYCLE = 5
    SECRET_KEY = 'what does the fox say?'

    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = get_redis_key()[0]
    CACHE_REDIS_PORT = get_redis_key()[1]
    CACHE_REDIS_DB = 8

httpcode_list = [
    200,
    404,
    500
]

condition_list = [
    "body",
    "args",
    "path",
    "header"
]

operation_list = [
    "contains",
    "equals"
]

method_list = [
    "GET",
    "POST",
    "PUT",
    "DELETE"
]

resp_type_list = [
    "application/json",
    "text/plain",
    "application/javascript",
    "application/xml",
    "text/xml",
    "text/html"
]
