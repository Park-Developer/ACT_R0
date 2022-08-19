import functools
from . import service
import web_tool
from config import ACT_logger
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user_info= web_tool.session_get(session_var=service.session_variable)

        if user_info is None:
            ACT_logger.error("login required action")
            return redirect(url_for("account.account_login"))
        return view(**kwargs)

    return wrapped_view