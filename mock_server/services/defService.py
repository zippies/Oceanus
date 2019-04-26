# -*- encoding:utf-8 -*-
from mock_server.models import Api, Condition
from mock_server import db, cache
from flask_login import current_user

def add_mock_service(request):
    data = request.json or request.form
    remote = data.get("remote")
    method = data.get("method")
    urlpath = data.get("urlpath")
    condition = data.get("condition")
    operation = data.get("operation")
    value = data.get("value")
    httpcode = data.get("httpcode")
    resp_type = data.get("resp_type")
    resp_body = data.get("resp_body")
    resp_default = data.get("resp_default")
    api = Api.query.filter_by(path=urlpath).filter_by(method=method).filter_by(status=0).first()
    if not api:
        api = Api(
            path=urlpath,
            method=method,
            resp_type=resp_type,
            httpcode=httpcode,
            resp_default=resp_default or resp_body,
            user_id=current_user.id if not remote else 1
        )
    if resp_default:
        api.resp_default = resp_default

    db.session.add(api)
    db.session.commit()

    if value:
        condition = Condition(
            api_id=api.id,
            condition=condition,
            operation=operation,
            value=value,
            httpcode=httpcode,
            resp_body=resp_body,
            user_id=current_user.id
        )
        db.session.add(condition)
    db.session.commit()
    cache.clear()


def edit_mock_service(id, request):
    api = Api.query.filter_by(id=id).first()
    force = request.form.get("force")
    if api:
        if force or api.user_id == current_user.id:
            resp_default = request.form.get("body")
            httpcode = request.form.get("httpcode")
            if resp_default:
                api.resp_default = resp_default
            if httpcode:
                api.httpcode = httpcode
            db.session.add(api)
            db.session.commit()
            cache.clear()
        else:
            raise Exception("只能编辑自己创建的mock-api")
    else:
        raise Exception("未配置的mock-api")


def edit_condition_resp(id, request):
    condition = Condition.query.filter_by(id=id).first()
    force = request.form.get("force")
    if condition:
        if force or condition.user_id == current_user.id:
            resp_body = request.form.get("body")
            httpcode = request.form.get("httpcode")
            value = request.form.get("value")
            if resp_body:
                condition.resp_body = resp_body
            if httpcode:
                condition.httpcode = httpcode
            if value:
                condition.value = value
            db.session.add(condition)
            db.session.commit()
            cache.clear()
        else:
            raise Exception("只能编辑自己创建的mock-api-condition")
    else:
        raise Exception("未配置的mock-api-condition")