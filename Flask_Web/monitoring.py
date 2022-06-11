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

app = Flask(__name__)
bp = Blueprint('monitoring', __name__, url_prefix='/monitoring')  # /monitoring/ ~\

trading_info=config.BOT_INFO # JSON Format

# [Index]
@bp.route('/')
def index():
    return render_template('monitoring/monitoring_index.html',trading_info=trading_info)


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



@bp.route('/get_curPrice')
async def get_curPrice():
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



