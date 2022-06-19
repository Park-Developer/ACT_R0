from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

# from Flask_Web.auth import login_required # 개발 필
import web_tool
from Flask_Web.db import get_db

bp = Blueprint('index', __name__)  # /monitoring/ ~\

@bp.route('/view_post')
def view_post():
    post_viewInfo={ # get data from URL parameter at index.html
        "post_title":request.args.get("title"),
        "post_created":request.args.get("created"),
        "post_author_id":request.args.get("author_id"),
        "post_index":request.args.get("index")
    }

    return render_template('home/view_post.html',post_viewInfo=post_viewInfo)

@bp.route('/new_post')
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
    # DEBUG -----------------------------------------------------------------------
    if request.method=='POST': # for debug
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        print("DB", db)
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
    # DEBUG -----------------------------------------------------------------------

    if request.method == 'GET':
        db = get_db() #  get_db returns a database connection, which is used to execute the commands read from the file.

        # users(db에 저장된 모든 user)
        users = db.execute(
            'SELECT * FROM user' # user table에서 모든 user 불러오기
        ).fetchall()
        print("users",users)

        # users(db에 저장된 모든 post)
        posts = db.execute(
            'SELECT * FROM post'  # post table에서 모든 post 불러오기
        ).fetchall()

    return render_template('index.html',posts=posts, users=users)


@bp.route('/new_post/save', methods=('GET', 'POST'))
#@login_required
def new_post_save():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            # writer 권한 검사
            author_id=web_tool.check_auth()

            # post DB에 정보 삽입
            db.execute(
                'INSERT INTO post (title, body,author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, author_id)
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


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
#@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('home/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
#@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('index.home'))