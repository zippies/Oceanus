# -*- encoding:utf-8 -*-
from flask import render_template, request, redirect, url_for, session
from config import condition_list, operation_list, method_list, resp_type_list, httpcode_list
from flask_login import login_user
from mock_server.models import User, db
from mock_server import gitlab
from mock_server.views import url


@url.route("/check_backend_active.html")
def nginx_check():
    return "i'm ok"


@url.route('/')
def home():
    if 'gitlab_token' in session:
        name = gitlab.get('user').data.get("email").split("@")[0]
        user = User.query.filter_by(nickname=name).first()
        if not user:
            user = User(
                nickname=name,
                ip=request.remote_addr
            )
            db.session.add(user)
            db.session.commit()

        login_user(user)
        return render_template(
            "index.html",
            user_name=user.nickname,
            httpcode_list=httpcode_list,
            condition_list=condition_list,
            operation_list=operation_list,
            method_list=method_list,
            resp_type_list=resp_type_list
        )
    return redirect(url_for('mock-server.login'))


@url.route('/login')
def login():
    return gitlab.authorize(callback=url_for('mock-server.authorized', _external=True, _scheme='http'))


@url.route('/logout')
def logout():
    del session['gitlab_token']
    return redirect(url_for('mock-server.index'))


@url.route('/login/authorized')
def authorized():
    resp = gitlab.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error'],
            request.args['error_description']
        )
    session['gitlab_token'] = (resp['access_token'], '')
    return redirect(url_for('mock-server.index'))


@gitlab.tokengetter
def get_gitlab_oauth_token():
    return session.get('gitlab_token')