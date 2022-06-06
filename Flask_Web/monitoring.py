from flask import (
    Blueprint, jsonify, flash, g, redirect, render_template, Response, request, session, url_for
)

import websockets
import asyncio
import json
import pyupbit
import pandas
import numpy
import time
bp = Blueprint('monitoring', __name__, url_prefix='/monitoring')  # /monitoring/ ~\
'''
async def upbit_ws_client():
    uri = "wss://api.upbit.com/websocket/v1"

    async with websockets.connect(uri,  ping_interval=60) as websocket:
        subscribe_fmt = [
            # Ticket Field
            {
                "ticket":"test"
            },

            # Type Field
            {
                "type": "ticker",
                "codes":["KRW-BTC"],
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
            await asyncio.sleep(1)
            data = json.loads(data)
            print(type(data["cd"]))
            yield data["cd"]


'''


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

# [Index]
@bp.route('/', methods=('GET', 'POST'))
def monitoring_main():
    print("[debug] monitoring_main")
    coin_info = " ? "
    return render_template('monitoring/monitoring_index.html', coin_info=coin_info)

