import functools

import config
import web_tool
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from Flask_Web.db import get_db

bp = Blueprint('account', __name__, url_prefix='/account')

@bp.route('/', methods=('GET', 'POST'))
def account_index():
    is_loginOK=web_tool # 로그인 여부

    ''' DB 관련 나줃에
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    '''
    if request.method == 'POST':
        check_data = {
            "data_type": config.ACCOUNT_CHECK_METHOD["CHECK_DATA_TYPE"],
            "user_list_address": config.ACCOUNT_CHECK_METHOD["USER_LIST_ADDRESS"],
            "access_code_address": config.ACCOUNT_CHECK_METHOD["ACCESS_CODE_ADDRESS"]
        }

        input_info={
            "email" :request.form['email'],
            "password" : request.form['password'],
            "access_code" : request.form['access_code']
        }

        if web_tool.check_account(input_info,check_data)==True: # 인증 성공
            print("CHEKC SUCCESS!!!")
        else: # 인증 실패
            flash("User Identification Fail!")
            print("CHEKC FAIL!!!")




    return render_template('auth/login.html',is_loginOK=is_loginOK)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')