# -*- encoding:utf-8 -*-
from flask import render_template, request, redirect, url_for
from config import condition_list, operation_list, method_list, resp_type_list, httpcode_list
from flask_login import login_user, logout_user, current_user
from mock_server.models import User, db
from mock_server.views import url
from flask_login import login_required


@url.route('/')
@login_required
def home():
    return render_template(
        "index.html",
        user_name=current_user.nickname,
        httpcode_list=httpcode_list,
        condition_list=condition_list,
        operation_list=operation_list,
        method_list=method_list,
        resp_type_list=resp_type_list
    )


@url.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        nickname = request.form.get("nickname")
        user = User.query.filter_by(nickname=nickname).first()
        if not user:
            user = User(nickname, request.remote_addr)
            db.session.add(user)
            db.session.commit()
        login_user(user)

        return redirect(request.args.get("next") or url_for("mock-server.index"))

    return render_template("login.html")


@url.route("/logout")
def logout():
    logout_user()
    return redirect("login")
