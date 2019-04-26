# -*- encoding:utf-8 -*-
from mock_server.models import Api, Condition
from flask import Response
from config import condition_list, cache_timeout
from mock_server import cache
import json
import re


def get_resp(r_type, r_body):

    res = None
    if r_type == "application/json":
        res = Response(json.dumps(json.loads(r_body)), mimetype=r_type)
        res.headers["Content-Type"] = r_type
    else:
        res = Response(r_body, mimetype=r_type)
    return res


def ismatch_body(resp_type, source, condition):
    operation = condition.operation
    value = condition.value
    resp_body = condition.resp_body
    http_code = condition.httpcode
    resp = get_resp(resp_type, resp_body)
    if operation == "=" or operation == "equals":
        if source == value:
            return True, resp, http_code
        else:
            return False, resp, http_code
    elif operation == "contains":
        if re.findall(value, str(source)):
            return True, resp, http_code
        else:
            return False, resp, http_code
    elif operation == "in":
        if source in value.split(","):
            return True, resp, http_code
        else:
            return False, resp, http_code
    else:
        return False, "no such option: %s" % operation, http_code


def get_matched_resp(resp_type, condition, request):
    body = request.json or dict(request.data) or dict(request.form)
    args = request.args
    header = str(request.headers)
    path = request.path

    when = condition.condition
    if when not in condition_list:
        return False, "no such condition: %s" % when
    else:
        return ismatch_body(resp_type, json.dumps(eval(when)), condition)


def get_mock_from_db(request):
    api = Api.query.filter_by(path=request.path).filter_by(method=request.method).filter_by(status=0).first()
    if api:
        conditions = Condition.query.filter_by(api_id=api.id).filter_by(status=0).all()
        for cdt in conditions:
            match, resp, httpcode = get_matched_resp(api.resp_type, cdt, request)
            if match:
                return resp, httpcode
        else:
            return get_resp(api.resp_type, api.resp_default), api.httpcode

    return "未配置的请求:" + request.path, 500


def get_mock_result_by_req(request):
    return get_mock_from_db(request)


@cache.cached(timeout=cache_timeout)
def get_cache_result_by_req(request):
    return get_mock_from_db(request)