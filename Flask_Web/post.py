from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

# from Flask_Web.auth import login_required # 개발 필
import web_tool
from Flask_Web.db import get_db
from Flask_Web import service
import functools
from config import ACT_logger

from . import login

bp = Blueprint('post', __name__)  # /monitoring/ ~\

@bp.route('/view_post/<int:post_id>/edit_post', methods=('GET','POST'))
@login.login_required
def edit_post(post_id):
    if request.method == 'GET':
        db = get_db()
        post = db.execute(
            f'SELECT * FROM post WHERE id={post_id}'  # post table에서 모든 post 불러오기
        ).fetchone()


        print("edit poist")
        # post_id : 게시물 index
        return render_template('home/edit_post.html',post=post,post_id=post_id)

@bp.route('/view_post/<int:post_id>/edit_save', methods=('GET','POST'))
@login.login_required
def save_edited_post(post_id):
    if request.method=='POST':
        # Read Form Data
        title = request.form['title']
        type = request.form['type']
        body = request.form['body']

        # Update DB
        db = get_db()
        db.execute(
            'UPDATE post SET title = ?, body = ?, type=?'
            ' WHERE id = ?',
            (title, body, type, post_id)
        )
        db.commit()

        return redirect(url_for("index.view_post",id=post_id))

    # return redirect(url_for("index.home"))

@bp.route('/find_post', methods=('GET','POST'))
def find_post():
    print("find post!")
    #return ('', 204) Return None
    return redirect(url_for("index.home"))