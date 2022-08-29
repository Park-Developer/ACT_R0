import functools
import config
import web_tool
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from Flask_Web import service
import re

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


    def extract_MinuteTime(data_type:str, time_data:str)->int:

        if ("Minute" in time_data) or ("minute" in time_data):
            time_unit=1
        elif ("Hour" in time_data) or ("hour" in time_data):
            time_unit=60
        elif ("Day" in time_data) or ("day" in time_data):
            time_unit = 60*24
        elif ("Week" in time_data) or ("week" in time_data):
            time_unit = 60*24*7

        if data_type=="period" or data_type=="Period":
            period=int(re.sub(r'[^0-9]','',time_data))

            return period*time_unit
        elif data_type=="dataunit" or data_type=="Dataunit":
            return time_unit

    if request.method == "POST":
        # Extract Integer Data from Request Form

        # (1) Training Data Setting
        training_peiod=extract_MinuteTime(data_type="period", time_data=request.form["training_period_select"])
        training_data_unit=extract_MinuteTime(data_type="dataunit", time_data=request.form["training_dataunit_select"])

        training_starttime_month = extract_NumberData_fromForm(request.form["training_starttime_month"])  # origin form : btraining_month_2
        training_starttime_day = extract_NumberData_fromForm(request.form["training_starttime_day"])  # origin form : btraining_day_5
        training_starttime_hour = extract_NumberData_fromForm(request.form["training_starttime_hour"])  # origin form : btraining_hour_3
        training_starttime_minute = extract_NumberData_fromForm(request.form["training_starttime_minute"])  # origin form : btraining_minute_4

        # (2) Backtesting Time Setting
        backtest_starttime_month =extract_NumberData_fromForm(request.form["backtest_starttime_month"])     # origin form : backstart_month_2
        backtest_starttime_day =extract_NumberData_fromForm(request.form["backtest_starttime_day"])         # origin form : backstart_day_5
        backtest_starttime_hour =extract_NumberData_fromForm(request.form["backtest_starttime_hour"])       # origin form : backstart_hour_3
        backtest_starttime_minute = extract_NumberData_fromForm(request.form["backtest_starttime_minute"])  # origin form : backstart_minute_4

        # Get Strategy Info
        strategyDB = web_tool.get_strategyInfo(strategy_name="테스트용")

        # Create Backesting Setting Data
        backtest_setting_data={
            # (1) tradining data
            "training_peiod":training_peiod,
            "training_data_unit":training_data_unit,

            # (2) simulation start time
            "backtest_starttime_year": datetime.datetime.now().date().strftime("%Y"),
            "backtest_starttime_month": backtest_starttime_month,
            "backtest_starttime_day": backtest_starttime_day,
            "backtest_starttime_hour": backtest_starttime_hour,
            "backtest_starttime_minute":  backtest_starttime_minute,

            # (2) training start time
            "training_starttime_year": datetime.datetime.now().date().strftime("%Y"),
            "training_starttime_month": training_starttime_month,
            "training_starttime_day": training_starttime_day,
            "training_starttime_hour": training_starttime_hour,
            "training_starttime_minute": training_starttime_minute,

            # (4) Strategy Data
            "monitoring_time": strategyDB["monitoring_time"],
    
        }

        # Get Strategy Info
        strategyDB = web_tool.get_strategyInfo(strategy_name="테스트용")

        return render_template('setting/backtest_run.html', login_userDB=login_userDB,
                                                            target_coin_id=target_coin_id,
                                                            backtest_setting_data=backtest_setting_data,
                                                            strategyDB=strategyDB)


@bp.route('/get_backtestData', methods=('GET','POST'))
def get_backtestData(): # btn_type : stop, restart
    # (1) Get Login User'DB Info
    login_userDB = web_tool.get_login_UserInfo(user_table="user_list",
                                               session_var=config.SESSION_VARIABLE)

    # (2) Get Request Data From JS(static/backtest/backtest_run.js simulate_backtest())
    # <User Setting Data>
    target_coin_id = request.args.get('target_coin_id', 0, type=int)
    market = request.args.get('market', 0, type=str)
    trading_period = request.args.get('trading_period', 0, type=str)
    trading_dataNumber = request.args.get('trading_dataNumber', 0, type=str)
    monitoring_time = request.args.get('monitoring_time', 0, type=str)

    # <Training Data>
    training_end_time= request.args.get('training_end_time', 0, type=str)
    training_unit= request.args.get('training_unit', 0, type=str)
    training_dataNumber= request.args.get('training_dataNumber', 0, type=str)

    # <Backtesting Data>
    simulation_end_time= request.args.get('simulation_end_time', 0, type=str)
    simulation_unit= request.args.get('simulation_unit', 0, type=str)
    simulation_dataNumber= request.args.get('simulation_dataNumber', 0, type=str)


    # (3) Create Training Data
    training_data=Upbit_Trade.upbit_tool.convert_pastData_to_Dict(market=market,
                                                         count=int(training_dataNumber),
                                                         data_unit=int(training_unit),to=training_end_time)

    # (4) Create Simulation Data
    backtest_data = Upbit_Trade.upbit_tool.convert_pastData_to_Dict(market=market,
                                                                    count=int(simulation_dataNumber),
                                                                    data_unit=int(simulation_unit),to=simulation_end_time)

    # (5) Analysis Training Data
    upbit_apiInfo, target_coinInfo=basic_tool.get_strategy_configData(target_coin_id, login_userDB)

    strategy_obj=basic_tool.get_strategy_clsObj(target_coinInfo)
    strategy_obj.load_configData(upbit_apiInfo=upbit_apiInfo,target_coinInfo=target_coinInfo)

    # backtest ON
    strategy_obj.backtest_modeON()

    # load training data to trading data
    strategy_obj.load_tradingData(training_data)
    strategy_obj.calc_ref_price()
    #print("strategy_obj.trading_data",strategy_obj.trading_data)
    print("ref price",strategy_obj.ref_price)
    strategy_obj.calc_Bid_max_Price()
    strategy_obj.calc_Ask_min_Price()
    print("self.bid_maxPrice",strategy_obj.bid_maxPrice)
    print("self.ask_minPrice",strategy_obj.ask_minPrice)



    # (6) Evaluate Simulation Data
    #print("------------------------RESPOND")
    #print(training_data)
    #print(backtest_data)
    #print("------------------------RESPOND")
    ref_data=[]
    bid_Maxdata=[]
    ask_Mindata=[]

    ref_dataNum=len(training_data["opening_price"])
    if strategy_obj.para_reference["dynamic_ref"]==False:
        ref_data=[strategy_obj.ref_price for i in range(ref_dataNum)]
    else:
        pass

    if strategy_obj.para_reference["dynamic_bid"] == False:
        bid_Maxdata=[strategy_obj.bid_maxPrice for i in range(ref_dataNum)]
    else:
        pass

    if strategy_obj.para_reference["dynamic_ask"] == False:
        ask_Mindata=[strategy_obj.ask_minPrice for i in range(ref_dataNum)]
    else:
        pass

    respond={
        "training_data":training_data,
        "backtest_data":backtest_data,

        "ref_price":strategy_obj.ref_price,
        "ref_price_data":ref_data,

        "bid_maxPrice":strategy_obj.bid_maxPrice,
        "bid_maxPrice_data":bid_Maxdata,

        "ask_minPrice":strategy_obj.ask_minPrice,
        "ask_minPrice_data":ask_Mindata
    }

    # (4) Load Trading Data

    return jsonify(respond)
