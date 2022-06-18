import config
from flask import (
    Blueprint, jsonify, flash, g, redirect, render_template, Response, request, session, url_for, Flask
)



bp = Blueprint('manage', __name__, url_prefix='/manage')  # /monitoring/ ~\

# [Index]
@bp.route('/')
def index():
    return render_template('manage.html')
