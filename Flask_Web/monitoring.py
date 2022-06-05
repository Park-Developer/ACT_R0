from flask import (
    Blueprint, flash, g, redirect, render_template,Response, request, session, url_for
)
import websockets
import asyncio
import json

bp = Blueprint('monitoring', __name__, url_prefix='/monitoring') # /monitoring/ ~\

@bp.route('/load_coinInfo', methods=('GET', 'POST')) #/monitoring/load_coinInfo
def load_coinInfo():
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
                web_data = await websocket.recv()

                data = json.loads(web_data)

                cur_coinInfo={
                    # <Ticker Respond>
                    "market_code" : data["cd"],
                    "current_cost" : data["tp"],
                    "recent_volumn" : data["tv"],
                    "time_stamp" : data["tms"],

                    # <Trade Respond>

                    # <Orderbook>
                    "ask_price" : data["ap"],
                    "bid_price" : data["bp"],
                    "ask_size" : data["as"],
                    "bid_size" : data["bs"],
                }
                yield data["tms"]

    async def main():
        await upbit_ws_client()

    asyncio.run(main())

    return Response(asyncio.run(main()), mimetype='text/plain')

@bp.route('/', methods=('GET', 'POST'))
def monitoring_main():
    print("[debug] monitoring_main")
    coin_info=" ? "
    return render_template('monitoring/monitoring_index.html',coin_info=coin_info)

