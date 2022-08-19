import functools
import config
import web_tool
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from Flask_Web import service

from werkzeug.security import generate_password_hash

from config import ACT_logger
from Flask_Web.db import get_db
import template_tool
from . import login

bp = Blueprint('account', __name__, url_prefix='/account')

@bp.route('/test', methods=('GET', 'POST'))
def test():
    return "TEST!-!"

@bp.route('/', methods=('GET', 'POST'))
@login.login_required
def account_index():
    login_userDB = web_tool.get_login_UserInfo(user_table="user_list", session_var=service.session_variable)

    return render_template('auth/account.html',login_userDB=login_userDB) # login 상태인 경우

@bp.route('/login', methods=('GET', 'POST'))
def account_login():
    if request.method == 'POST':
        # User Input Data
        input_info={
            "email" :request.form['email'],
            "password" : request.form['password'],
        }
        # Account Check
        db = get_db()
        is_confirmed, user_db=web_tool.check_account("user_list",input_info,db) # user 확인 성공
        if is_confirmed==True:
            login_userInfo = template_tool.convert_DB_to_UserInfo(user_db)
            web_tool.session_update(session_var=service.session_variable, session_data=login_userInfo)

            login_userDB=web_tool.get_login_UserInfo(user_table="user_list", session_var=service.session_variable)

            return render_template('auth/account.html', login_userDB=login_userDB)

        else:
            return render_template('auth/login.html')

    elif request.method == 'GET':
        return render_template('auth/login.html')

@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    web_tool.session_clear()

    return redirect(url_for('account.account_index'))


@bp.route('/manage', methods=('GET', 'POST'))
def manage():
    if request.method == 'GET':
        return render_template('manage.html')

'''
[REGISTER]
'''
@bp.route('/register', methods=('GET', 'POST'))
def register():
    return render_template('auth/register.html')

@bp.route('/register/ok', methods=('GET', 'POST')) #
def register_ok():
    print("register ok")
    if request.method == 'POST':  # for debug
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        print("REGISTER")
        print(username)
        print(email)
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user_list (username, password,email) VALUES (?,?, ?)",
                    (username, generate_password_hash(password),email),
                )

                db.commit()

            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("index.home"))

        flash(error)

        return redirect(url_for('index.home')) # Home으로 이동
