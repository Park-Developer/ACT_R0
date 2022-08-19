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

# websocket test
import asyncio
import datetime
import random
import websockets
import json

from . import login

bp = Blueprint('index', __name__)  # /monitoring/ ~\

'''
POST를 클릭했을때의 이동 URL 대응 함수
'''
@bp.route('/view_post/<int:id>', methods=('GET', 'POST'))
@login.login_required
def view_post(id):
    if request.method == 'GET':
        db = get_db()

        # [1] Get Post Data
        post = db.execute(
            f'SELECT * FROM post WHERE id={id}'  # post table에서 모든 post 불러오기
        ).fetchone()

        # [2] Get User Data
        user_Info=web_tool.get_login_UserInfo(user_table="user_list",session_var=service.session_variable)

        # User View Check
        user_writeList=user_Info["write_post"].split(",")
        user_likeList=user_Info["like_post"].split(",")
        user_dislikeList=user_Info["dislike_post"].split(",")

        User_postInfo={}
        # (1) 작성여부 확인
        if str(id) in user_writeList:
            User_postInfo["is_writePost"] =True
        else:
            User_postInfo["is_writePost"] = False

        # (2) like여부 확인
        if str(id) in user_likeList:
            User_postInfo["is_likePost"]=True
        else:
            User_postInfo["is_likePost"] = False

        # (3) dislike여부 확인
        if str(id) in user_dislikeList:
            User_postInfo["is_dislikePost"] =True
        else:
            User_postInfo["is_dislikePost"] = False
        print("User_postInfo",User_postInfo)

    return render_template('home/view_post.html', post=post, User_postInfo=User_postInfo)

@bp.route('/new_post')
@login.login_required
def new_post():
    print("PSTO JEW") #debug
    return render_template('home/new_post.html')

@bp.route('/debug') # Index Page
def debug():
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
            return redirect(url_for("index.home"))

    flash(error)


    return redirect(url_for('index.home'))


@bp.route('/',methods=('GET','POST')) # Index Page
def home():
    if request.method == 'GET':
        db = get_db() #  get_db returns a database connection, which is used to execute the commands read from the file.

        # users(db에 저장된 모든 user)
        users = db.execute(
            'SELECT * FROM user_list' # user table에서 모든 user 불러오기
        ).fetchall()
        print("users",users)

        # users(db에 저장된 모든 post)
        posts = db.execute(
            'SELECT * FROM post'  # post table에서 모든 post 불러오기
        ).fetchall()

    elif request.method == 'POST':
        print("HOME PIST!!")
        print(request.form)
        db = get_db()  # get_db returns a database connection, which is used to execute the commands read from the file.

        # users(db에 저장된 모든 user)
        users = db.execute(
            'SELECT * FROM user_list'  # user table에서 모든 user 불러오기
        ).fetchall()


        # users(db에 저장된 모든 post)
        posts = db.execute(
            'SELECT * FROM post'  # post table에서 모든 post 불러오기
        ).fetchall()

    return render_template('index.html',posts=posts, users=users)


@bp.route('/new_post/save', methods=('GET', 'POST'))
@login.login_required
def new_post_save():
    if request.method == 'POST':
        print("new_post_SAbv")
        print(request.form)
        try:
            title = request.form['title']
            body = request.form['body']
            type=request.form['type']
            author_id=web_tool.get_login_username(session_var=service.session_variable)
        except KeyError as key:
            ACT_logger.error("key_err : request key error")

        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()

            # post DB에 정보 삽입
            db.execute(
                'INSERT INTO post (title, body,type,author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, type, author_id)
            )
            db.commit()
            return redirect(url_for('index.home'))

    return render_template('home/new_post.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/delete', methods=('POST',))
#@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('index.home'))


# Websocket Test
