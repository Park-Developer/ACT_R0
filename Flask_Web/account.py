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

    # SESSION GET

    user_info = web_tool.session_get(session_var=service.session_variable)  # SESSION USER_ID {'access_code': '7U852X89', 'email': 'parkwonho94@gmail.com', 'password': 'wonho123', 'username': 'master'}

    if user_info==None:
        return render_template('auth/login.html') # user_id가 없는 경우 login.html retrun
    else:
        print("lgoing")
        print(user_info)
        return render_template('auth/account.html',user_info=user_info) # login 상태인 경우

@bp.route('/login', methods=('GET', 'POST'))
def account_login():
    if request.method == 'POST':
        # User Input Data
        input_info={
            "email" :request.form['email'],
            "password" : request.form['password'],
            "access_code" : request.form['access_code'] # 일단 비교안함
        }
        print("saDWASDASDASDASD")
        # Account Check
        db = get_db()
        is_confirmed, user_db=web_tool.check_account("user_list",input_info,db) # user 확인 성공
        if is_confirmed==True:
            user_info = template_tool.convert_DB_to_UserInfo(user_db)
            web_tool.session_update(session_var=service.session_variable, session_data=user_info)

            print("USERER",user_info)
            return render_template('auth/account.html', user_info=user_info)
        else:
            return render_template('auth/login.html')

    elif request.method == 'GET':
        return render_template('auth/login.html')

@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    web_tool.session_clear()

    return redirect(url_for('account.account_index'))



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

