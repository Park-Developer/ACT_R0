import config
from flask import (
    Blueprint, jsonify, flash, g, redirect, render_template, Response, request, session, url_for, Flask
)
import websockets
import asyncio
import json
import pyupbit
import pandas
import numpy
import time

from Flask_Web import service, login
import web_tool

app = Flask(__name__)
bp = Blueprint('monitoring', __name__, url_prefix='/monitoring')  # /monitoring/ ~\

trading_info=config.BOT_INFO # JSON Format

# test
@bp.route('/test')
def test():
    return jsonify({"asd":111,"bbb":222})
# test
# [Index]
@bp.route('/')
@login.login_required
def index():
    target_coin_id=1 # default : 1

    login_userDB = web_tool.get_login_UserInfo(user_table="user_list", session_var=service.session_variable)
    return render_template('monitoring/monitoring_index.html',
                           login_userDB=login_userDB,
                           trading_info=trading_info,
                           target_coin_id=target_coin_id)


# [Real Time Coin Data Load]
@bp.route('/load_coinInfo', methods=('GET', 'POST'))  # /monitoring/load_coinInfo
def load_coinInfo():
    print("[debug] load_coinInfo")

    d = {"name": "홍길동", "birth": "0525", "age": "30"}

    response = Response(

        response=json.dumps(d),

        status=200,

        mimetype='application/json'
    )
    return response

@bp.route('/target_coin<int:target_id>',methods=('POST','GET' ))
@login.login_required
def show_targetInfo(target_id):
    target_coin_id = target_id

    login_userDB = web_tool.get_login_UserInfo(user_table="user_list", session_var=service.session_variable)
    return render_template('monitoring/monitoring_index.html',
                           login_userDB=login_userDB,
                           trading_info=trading_info,
                           target_coin_id=target_coin_id)

@bp.route('/get_curPrice')
async def get_curPrice():
    #get(key, default=None, type=None)
    coin_ticker = request.args.get('coin_ticker', 0, type=str)
    #b = request.args.get('b', 0, type=int)

    uri = "wss://api.upbit.com/websocket/v1" # API Address

    async with websockets.connect(uri,  ping_interval=60) as websocket:
        subscribe_fmt = [
            # Ticket Field
            {
                "ticket":"test"
            },
            # Type Field
            {
                "type": "ticker",
                "codes":[coin_ticker],
                "isOnlyRealtime": True
            },
            # Format Field
            {
                "format":"SIMPLE"
            }
        ]
        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)

        while True:
            data = await websocket.recv()
            data = json.loads(data)
            cur_price = data["tp"]
            print(cur_price)
            return jsonify(cur_price)



