from flask import (
    Blueprint, jsonify, flash, g, redirect, render_template, Response, request, session, url_for
)


bp = Blueprint('index', __name__)  # /monitoring/ ~\

@bp.route('/') # Index Page
def home():
    return render_template('index.html')

