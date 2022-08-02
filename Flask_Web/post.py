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

@bp.route('/view_post/<int:post_id>/like', methods=('GET','POST'))
@login.login_required
def like_post(post_id:int): # post_id를 string으로 변환해야함
    like_number=0 # post table에서 증감 계산
    dislike_number=0

    # [1] Get Login User Data
    db = get_db()
    user_Info = web_tool.get_login_UserInfo(user_table="user_list", session_var=service.session_variable)

    # [2] Update User's Likelist
    user_like_list=user_Info['like_post'].split(',')
    user_dislike_list = user_Info['dislike_post'].split(',')

    if str(post_id) in user_like_list:
        user_like_list.remove(str(post_id)) # 이미 like가 눌러져있는 경우 취소하기
        like_number=-1
    else:
        user_like_list.append(str(post_id)) # like가 눌러져있지 않은 경우 추가하기
        like_number = +1

        if str(post_id) in user_dislike_list:
            user_dislike_list.remove(str(post_id))
            dislike_number = -1
    print("user_like_list", user_like_list)
    print("user_dislike_list",user_dislike_list)

    db.execute( 'UPDATE user_list SET like_post = ?, dislike_post = ?'
                ' WHERE access_code = ?',
                (",".join(user_like_list), ",".join(user_dislike_list), user_Info["access_code"])
    )
    db.commit()

    # [3] Update Post's Likelist
    db.execute( 'UPDATE post SET like_num = like_num + ?, dislike_num = dislike_num + ?'
                ' WHERE id = ?',
                (like_number,dislike_number,post_id)
    )
    db.commit()

    return redirect(url_for('index.view_post',id=post_id))

@bp.route('/view_post/<int:post_id>/dislike', methods=('GET', 'POST'))
@login.login_required
def dislike_post(post_id):
    like_number=0 # post table에서 증감 계산
    dislike_number=0

    # [1] Get Login User Data
    db = get_db()
    user_Info = web_tool.get_login_UserInfo(user_table="user_list", session_var=service.session_variable)

    # [2] Update User's Likelist
    user_like_list=user_Info['like_post'].split(',')
    user_dislike_list = user_Info['dislike_post'].split(',')

    if str(post_id) in user_dislike_list:
        user_dislike_list.remove(str(post_id)) # 이미 like가 눌러져있는 경우 취소하기
        dislike_number=-1
    else:
        user_dislike_list.append(str(post_id)) # like가 눌러져있지 않은 경우 추가하기
        dislike_number = +1

        if str(post_id) in user_like_list:
            user_like_list.remove(str(post_id))
            like_number = -1
    print("user_like_list", user_like_list)
    print("user_dislike_list",user_dislike_list)

    db.execute( 'UPDATE user_list SET like_post = ?, dislike_post = ?'
                ' WHERE access_code = ?',
                (",".join(user_like_list), ",".join(user_dislike_list), user_Info["access_code"])
    )
    db.commit()

    # [3] Update Post's Dislikelist
    db.execute( 'UPDATE post SET like_num = like_num + ?, dislike_num = dislike_num + ?'
                ' WHERE id = ?',
                (like_number,dislike_number,post_id)
    )
    db.commit()

    return redirect(url_for('index.view_post',id=post_id))

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