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
import datetime
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


    # Get Request Form : <form action="/backtest/target_{{target_coin_id}}/run" method="post">
    def extract_NumberData_fromForm(form_data: str) -> str:
        number_Data = form_data.split("_")[2]

        if (len(number_Data) == 1):
            return "0" + number_Data
        else:
            return number_Data


    if request.method == "POST":
        # Extract Integer Data from Request Form
        backtest_starttime_month =extract_NumberData_fromForm(request.form["backtest_starttime_month"])     # origin form : backstart_month_2
        backtest_starttime_day =extract_NumberData_fromForm(request.form["backtest_starttime_day"])         # origin form : backstart_day_5
        backtest_starttime_hour =extract_NumberData_fromForm(request.form["backtest_starttime_hour"])       # origin form : backstart_hour_3
        backtest_starttime_minute = extract_NumberData_fromForm(request.form["backtest_starttime_minute"])  # origin form : backstart_minute_4

        training_starttime_month =extract_NumberData_fromForm(request.form["training_starttime_month"])     # origin form : backstart_month_2
        training_starttime_day =extract_NumberData_fromForm(request.form["training_starttime_day"])         # origin form : backstart_day_5
        training_starttime_hour =extract_NumberData_fromForm(request.form["training_starttime_hour"])       # origin form : backstart_hour_3
        training_starttime_minute = extract_NumberData_fromForm(request.form["training_starttime_minute"])  # origin form : backstart_minute_4

        # Get Strategy Info
        strategyDB = web_tool.get_strategyInfo(strategy_name="테스트용")

        # Create Backesting Setting Data
        backtest_setting_data={
            # (1) tradining data

            # (2) simulation start time
            "backtest_starttime_year": datetime.datetime.now().date().strftime("%Y"),
            "backtest_starttime_month": backtest_starttime_month,
            "backtest_starttime_day": backtest_starttime_day,
            "backtest_starttime_hour": backtest_starttime_hour,
            "backtest_starttime_minute":  backtest_starttime_minute,

            # (2) simulation start time
            "training_starttime_year": datetime.datetime.now().date().strftime("%Y"),
            "training_starttime_month": training_starttime_month,
            "training_starttime_day": training_starttime_day,
            "training_starttime_hour": training_starttime_hour,
            "training_starttime_minute": training_starttime_minute,

            # (4) Strategy Data
            "monitoring_time": strategyDB["monitoring_time"],
            
            # (5) test env
            "test_speed" : request.form["test_speed"]
        }

        return render_template('setting/backtest_run.html', login_userDB=login_userDB,
                                                            target_coin_id=target_coin_id,
                                                            backtest_setting_data=backtest_setting_data)


@bp.route('/get_backtestData', methods=('GET','POST'))
def get_backtestData(): # btn_type : stop, restart
    # (1) Get Login User'DB Info
    login_userDB = web_tool.get_login_UserInfo(user_table="user_list",
                                               session_var=config.SESSION_VARIABLE)

    # (2) Get Request Data From JS
    target_coin_id = request.args.get('target_coin_id', 0, type=int)
    market=request.args.get('market', 0, type=str)
    count=request.args.get('data_number', 0, type=int)
    data_unit=request.args.get('data_unit', 0, type=str)
    monitoring_time=request.args.get('monitoring_time', 0, type=str)
    training_end_time=request.args.get('training_end_time', 0, type=str)
    simulation_end_time=request.args.get('simulation_end_time', 0, type=str)

    print("count",count,"  data_unit",  data_unit)
    # (3) Create Trading Data
    training_data=Upbit_Trade.upbit_tool.convert_pastData_to_Dict(market=market,
                                                         count=count,
                                                         data_unit=data_unit,to=training_end_time)


    # (3) Create Trading Data
    backtest_data = Upbit_Trade.upbit_tool.convert_pastData_to_Dict(market=market,
                                                                    count=count,
                                                                    data_unit=data_unit, to=simulation_end_time)

    respond={
        "training_data":training_data,
        "backtest_data":backtest_data
    }
    print( respond)
    # (4) Load Trading Data

    return jsonify(respond)
