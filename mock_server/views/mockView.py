# -*- encoding:utf-8 -*-
from flask import request
from mock_server.services.mockService import get_mock_result_by_req, get_cache_result_by_req
from mock_server import logger, cache
from mock_server.views import url
from config import cache_timeout


@cache.cached(timeout=cache_timeout)
@url.route("/<regex('[\w\W]*'):path>", methods=["GET", "POST", "HEAD", "OPTIONS", "PUT", "DELETE"])
def route(path):
    logger.info("%s\n[%s]调用: %s [参数]: %s" % ("-"*100, request.method, request.path, request.args))
    logger.info("[BODY]:\n%s" % request.data)
    logger.info("[HEADERS]: %s" % request.headers)

    if request.args.get("cache"):
        return get_cache_result_by_req(request)
    return get_mock_result_by_req(request)
