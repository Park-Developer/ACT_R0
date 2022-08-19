from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

# from Flask_Web.auth import login_required # 개발 필
import web_tool
from Flask_Web.db import get_db
from Flask_Web import service
from config import ACT_logger

from . import login

bp = Blueprint('server', __name__)

@bp.route('/', methods=('GET', 'POST'))
@login.login_required
def index():
    login_userDB = web_tool.get_login_UserInfo(user_table="user_list", session_var=service.session_variable)

    return render_template('auth/account.html',login_userDB=login_userDB) # login 상태인 경우
