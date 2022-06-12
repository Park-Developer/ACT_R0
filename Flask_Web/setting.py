import config
from flask import (
    Blueprint, jsonify, flash, g, redirect, render_template, Response, request, session, url_for, Flask
)


app = Flask(__name__)
bp = Blueprint('setting', __name__, url_prefix='/setting')  # /monitoring/ ~\

# [Index]
@bp.route('/')
def index():
    return render_template('setting.html')
