import functools
import config
import web_tool
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from Flask_Web import service

from werkzeug.security import generate_password_hash

from config import ACT_logger
from Flask_Web.db import get_db
import template_tool
from . import login
import basic_tool

# Tradig Pkg Import
import Upbit_Trade # Trading Config
import Upbit_Trade.Strategy1 # Strategy1

bp = Blueprint('backtest', __name__, url_prefix='/backtest')


@bp.route('/target_<int:target_coin_id>/setting', methods=('GET','POST'))
@login.login_required
def set_backtest(target_coin_id): # btn_type : stop, restart
    # Get Login User'DB Info
    login_userDB = web_tool.get_login_UserInfo(user_table="user_list", session_var=service.session_variable)

    # Get Strategy Info
    strategyDB=web_tool.get_strategyInfo(strategy_name="테스트용")

    return render_template('setting/backtest_setting.html',login_userDB=login_userDB,target_coin_id=target_coin_id,strategyDB=strategyDB)

@bp.route('/target_<int:target_coin_id>/run', methods=('GET','POST'))
@login.login_required
def backtest_run(target_coin_id):
    # Get Login User'DB Info
    login_userDB = web_tool.get_login_UserInfo(user_table="user_list", session_var=service.session_variable)

    # Get Request Form
    if request.method == "POST":
        request_data={
            "data_unit" : request.form["data_unit"],
            "data_number" : request.form["data_number"],
            "test_speed" : request.form["test_speed"]
        }

        return render_template('setting/backtest_run.html', login_userDB=login_userDB,
                                                            target_coin_id=target_coin_id,
                                                            request_data=request_data)


@bp.route('/get_backtestData', methods=('GET','POST'))
def get_backtestData(): # btn_type : stop, restart
    # (1) Get Request Data From JS
    market=request.args.get('market', 0, type=str)
    count=request.args.get('data_number', 0, type=int)
    data_unit=request.args.get('data_unit', 0, type=str)
    target_coin_id=request.args.get('target_coin_id', 0, type=int)

    '''(old)
    converted_pastData=Upbit_Trade.upbit_tool.convert_pastData_to_Dict(market=market,
                                                         count=count,
                                                         data_unit=data_unit)
    '''
    # Get Login User'DB Info
    login_userDB = web_tool.get_login_UserInfo(user_table="user_list",
                                               session_var=config.SESSION_VARIABLE)


    # (2) Create Upbit Trading Obj
    strategy_obj=basic_tool.get_trading_strategy_Obj(target_coin_id=target_coin_id,
                                                     login_userDB=login_userDB)
    print(strategy_obj.get_strategyInfo())

    # (3) Create Trading Data
    backtest_data=Upbit_Trade.upbit_tool.convert_pastData_to_Dict(market=market,
                                                         count=count,
                                                         data_unit=data_unit)

    # (4) Load Trading Data

    '''
    # get trading data
    strategy_obj.coin_info.get_tradingData(backtest_data)

    #print("Trading Data : ",strategy_obj.coin_info.trading_data)

    print("Calc ref_price",strategy_obj.calc_ref_price())
    print("self.coin_info.ref_price", strategy_obj.coin_info.ref_price)
    print("calc_Bid_max_Price",strategy_obj.calc_Bid_max_Price())
    print("calc_Ask_min_Price",strategy_obj.calc_Ask_min_Price())

    print(strategy_obj.coin_info.get_tradingData())
    '''
    return jsonify(backtest_data)
