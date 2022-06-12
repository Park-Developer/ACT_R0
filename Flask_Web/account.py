import functools

import basic_tool
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
    user_id = session.get('user_id')

    if user_id==None:
        return render_template('auth/login.html') # user_id가 없는 경우 login.html retrun
    else:
        return render_template('auth/account.html')

@bp.route('/login', methods=('GET', 'POST'))
def account_login():
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
        session_info={}
        if web_tool.check_account(input_info,check_data)==True: # 인증 성공
            print("CHEKC SUCCESS!!!")
            is_in_user, username=basic_tool.check_username(check_data["user_list_address"],input_info["email"])
            if is_in_user==True:
                session_info.update(input_info)
                session_info["username"]=username

                session['user_id']=session_info # 입력받은 유저 정보
                return render_template('auth/account.html')
            else:
                flash("Abnormal User Error!")

        else: # 인증 실패
            flash("User Identification Fail!")
            print("CHEKC FAIL!!!")

    return render_template('auth/login.html')

'''
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
'''
@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return redirect(url_for('account.account_index'))
    #return render_template('auth/account.html')


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