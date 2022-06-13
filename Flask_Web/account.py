import functools
import upbit_tool
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

    # SESSION GET
    user_info = web_tool.session_get(session_var=config.ACCOUNT_CHECK_METHOD["SESSION_VARIABLE"])  # SESSION USER_ID {'access_code': '7U852X89', 'email': 'parkwonho94@gmail.com', 'password': 'wonho123', 'username': 'master'}

    print("SESSION USER_ID",user_info)

    if user_info==None:
        return render_template('auth/login.html') # user_id가 없는 경우 login.html retrun
    else:
        return render_template('auth/account.html',user_info=user_info) # login 상태인 경우

@bp.route('/login', methods=('GET', 'POST'))
def account_login():
    if request.method == 'POST':
        # Server Storing Data For Check
        check_data = {
            "data_type": config.ACCOUNT_CHECK_METHOD["CHECK_DATA_TYPE"],
            "user_list_address": config.ACCOUNT_CHECK_METHOD["USER_LIST_ADDRESS"],
        }

        # User Input Data
        input_info={
            "email" :request.form['email'],
            "password" : request.form['password'],
            "access_code" : request.form['access_code']
        }

        if web_tool.check_account(input_info,check_data)==True: # 인증 성공
            print("CHEKC SUCCESS!!!")
            # [1] Get User Info(static user info + dynamic user info)
            user_info=basic_tool.get_userInfo(email=input_info["email"],
                                              data_addr=config.ACCOUNT_CHECK_METHOD["USER_LIST_ADDRESS"],
                                              read_method="JSON"
                                              )

            # [2] SESSION Update
            web_tool.session_update(session_var=config.ACCOUNT_CHECK_METHOD["SESSION_VARIABLE"], session_data=user_info)

            return render_template('auth/account.html',user_info=user_info)

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
    web_tool.session_clear()

    return redirect(url_for('account.account_index'))


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
