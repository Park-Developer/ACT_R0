import config
from flask import (
    Blueprint, jsonify, flash, g, redirect, render_template, Response, request, session, url_for, Flask
)


app = Flask(__name__)
bp = Blueprint('qna', __name__, url_prefix='/QnA')  # /monitoring/ ~\

# [Index]
@bp.route('/')
def index():
    return render_template('qna.html')
