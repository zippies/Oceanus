# -*- encoding:utf-8 -*-
from flask import request, jsonify
from mock_server.models import Api, Condition
from mock_server.services.common import response
from mock_server.services.defService import add_mock_service, edit_mock_service, edit_condition_resp
from flask_login import current_user
from mock_server import db, cache
from mock_server.views import url
import traceback


@url.route("/addmock", methods=["POST"])
def addMock():
    try:
        add_mock_service(request)
    except Exception as e:
        print traceback.format_exc()
        return response(success=False, error=str(e))
    return response()


@url.route("/mock/all")
def mocks():
    apis = Api.query.filter_by(status=0).all()
    return jsonify([api.to_json() for api in apis])


@url.route("/mock/delete/<int:id>", methods=["DELETE"])
def deleteMock(id):
    api = Api.query.filter_by(id=id).first()
    if api and api.user_id == current_user.id:
        conditions = Condition.query.filter_by(user_id=current_user.id).filter_by(api_id=id).all()
        api.status = -1
        db.session.add(api)
        for c in conditions:
            c.status = -1
            db.session.add(c)
        db.session.commit()
        cache.clear()
        return response()
    elif api:
        return response(False, "只能删除自己创建的mock-api")
    else:
        return response(False, "未配置的mock-api")


@url.route("/mock/<int:apiid>/conditions")
def getApiConditions(apiid):
    conditions = Condition.query.filter_by(status=0).filter_by(api_id=apiid).all()
    return jsonify([c.to_json() for c in conditions])


@url.route("/condition/delete/<int:id>", methods=["DELETE"])
def deleteCondition(id):
    condition = Condition.query.filter_by(id=id).first()
    if condition and condition.user_id == current_user.id:
        condition.status = -1
        db.session.add(condition)
        db.session.commit()
        cache.clear()
        return response()
    elif condition:
        return response(False, "只能删除自己创建的mock-api-condition")
    else:
        return response(False, "未配置的mock-api-condition")


@url.route("/mock/edit/<int:apiid>", methods=["PUT"])
def editMockApiBody(apiid):
    try:
        edit_mock_service(apiid, request)
    except Exception as e:
        return response(False, str(e))

    return response()


@url.route("/condition/edit/<int:condition_id>", methods=["PUT"])
def editConditionBody(condition_id):
    try:
        edit_condition_resp(condition_id, request)
    except Exception as e:
        return response(False, str(e))
    return response()