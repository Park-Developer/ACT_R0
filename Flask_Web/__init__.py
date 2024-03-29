import os
import sys
from flask import Flask

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
print("current dit",currentdir)
parentdir = os.path.dirname(currentdir)
print("paremt dit",parentdir)
sys.path.insert(0,parentdir)

import config

master = config.Master()
service= config.Service()



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'Flask_Web.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello[For test]
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # blueprint Register
    from . import index
    app.register_blueprint(index.bp)

    from . import db
    db.init_app(app)

    from . import account
    app.register_blueprint(account.bp)

    from . import monitoring
    app.register_blueprint(monitoring.bp)

    from . import qna
    app.register_blueprint(qna.bp)

    from . import post
    app.register_blueprint(post.bp)

    from . import manage
    app.register_blueprint(manage.bp)

    from . import setting
    app.register_blueprint(setting.bp)

    from . import server
    app.register_blueprint(server.bp)

    from . import backtest
    app.register_blueprint(backtest.bp)

    # CLI Register
    from . import cli
    cli.make_CLI(app) # CLI 생성

    return app
