import config
from flask import (
    Blueprint, jsonify, flash, g, redirect, render_template, Response, request, session, url_for, Flask
)
from . import login, service
import web_tool
from Flask_Web.db import get_db
app = Flask(__name__)
bp = Blueprint('setting', __name__, url_prefix='/setting')  # /monitoring/ ~\

# [Index]
@bp.route('/')
@login.login_required
def index():
    login_userInfo=web_tool.session_get(session_var=service.session_variable)
    login_userEmail=login_userInfo["email"]
    server_db = get_db()
    db_table="user_list"

    login_userDB=web_tool.get_loginUserInfo(login_userEmail,server_db,db_table)

    print("setting user")
    print(login_userInfo)
    return render_template('setting.html',login_userDB=login_userDB)

@bp.route('/save')
@login.login_required
def save_setting():
    login_userInfo=web_tool.session_get(session_var=service.session_variable)
    login_userEmail=login_userInfo["email"]
    server_db = get_db()
    db_table="user_list"

    login_userDB=web_tool.get_loginUserInfo(login_userEmail,server_db,db_table)

    print("setting user")
    print(login_userInfo)
    return render_template('setting.html',login_userDB=login_userDB)
