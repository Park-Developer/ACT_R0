import Upbit_Trade.upbit_tool
import basic_tool
import config
from flask import (
    Blueprint, jsonify, flash, g, redirect, render_template, Response, request, session, url_for, Flask
)
from . import login, service
import web_tool
from Flask_Web.db import get_db
from Upbit_Trade.Strategy1 import STRATEGY1_CONFIG_DATA # strategy1 config json address
from flask import Flask, g

from multiprocessing import Process


app = Flask(__name__)
bp = Blueprint('setting', __name__, url_prefix='/setting')  # /monitoring/ ~\

def fun(name):
    for i in range(3):
        print(f'hello {name}')



@bp.route('/test')
def test():
    return jsonify({"asd":111,"bbb":222})

# [Index]
@bp.route('/')
@login.login_required
def index():
    # Get Login User'DB Info
    login_userDB=web_tool.get_login_UserInfo(user_table="user_list",session_var=service.session_variable)

    setting_coin_list={
        "target_coin1":False,
        "target_coin2": False,
        "target_coin3": False,
        "target_coin4": False,
        "target_coin5": False,
    }

    p = Process(target=fun, args=('Peter',))
    p.start()

    # mulio test
    return render_template('setting/setting.html',login_userDB=login_userDB,setting_coin_list=setting_coin_list)

@bp.route('/coin/<int:target_coin_id>')
@login.login_required
def set_coin(target_coin_id):
    # Get Login User'DB Info
    login_userDB=web_tool.get_login_UserInfo(user_table="user_list",session_var=service.session_variable)

    setting_coin_list={
        "target_coin1":False,
        "target_coin2": False,
        "target_coin3": False,
        "target_coin4": False,
        "target_coin5": False,
    }

    setting_coin_list[f"target_coin{target_coin_id}"]=True

    market_list=Upbit_Trade.upbit_tool.get_UPBIT_marketlist(warning_filter=True)

    return render_template('setting/setting.html',login_userDB=login_userDB,setting_coin_list=setting_coin_list,market_list=market_list)


def read_setting_period(period_data:str)->tuple:
    # user가 설정한 period 데이터를 분 단위로 반환

    # 공백제거
    v1=period_data.replace(" ","")

    # 튜플형 시간 데이터 반황 (Days, Hours, Minutes)
    if ("hour" in v1) or ("Hour" in v1):
        v1=v1.replace("hour","")
        v1=v1.replace("Hour","")

        return (0,int(v1),0)
    elif ("day" in v1) or ("Day" in v1):
        v1=v1.replace("day","")
        v1=v1.replace("Day","")

        return (int(v1),0,0)
    elif ("week" in v1) or ("Week" in v1):
        v1=v1.replace("week","")
        v1=v1.replace("Week","")

        return (int(v1)*7,0,0)
    else:
        print("ead_setting_period(period_data:str) ERRIR!!1")

def check_setting_req_Data(request_data):
    # [1] Required Data Check
    required_para=["market","period","strategy","principal"]
    for rq_para in required_para:
        if request_data[rq_para]=="Required":
            flash("Please required parameter check")
            return False

        if rq_para=="principal": # principal 추가 조건
            if request_data[rq_para].strip().isdigit() == False:
                flash("Please required parameter check")
                return False

    # [2] Input Data Check

    return True


# Button Type에 따른 처리 : stop / restart
@bp.route('/coin/<int:target_coin_id>/<string:btn_type>', methods=('GET','POST'))
@login.login_required
def stop_coinRunning(target_coin_id,btn_type): # btn_type : stop, restart
    if request.method=="GET":
        # Decide Parameter Value
        if btn_type=="stop":
            is_tradingStop__val=True
        elif btn_type=="restart":
            is_tradingStop__val = False

        # Get Login User'DB Info
        login_userDB=web_tool.get_login_UserInfo(user_table="user_list",session_var=service.session_variable)

        # Change Parameter1
        login_userDB[f"target_coin{target_coin_id}"]["is_tradingStop"]=is_tradingStop__val

        # Change Parameter2
        current_time=basic_tool.get_current_kst_Time()
        if btn_type=="stop":
            login_userDB[f"target_coin{target_coin_id}"]["stop_time"] = current_time
        elif btn_type=="restart":
            login_userDB[f"target_coin{target_coin_id}"]["restart_time"] = current_time

        # Converted to MySQLJSON
        updated_target_data=basic_tool.convert_dict_to_MySQLjson(login_userDB[f"target_coin{target_coin_id}"])

        # DB Update
        update_query_cmd=f"UPDATE user_list SET target_coin{target_coin_id} = ? WHERE access_code = ?"
        update_data=(
            updated_target_data,
            login_userDB["access_code"]
        )

        db = get_db()
        db.execute(update_query_cmd, update_data)
        db.commit()

        return redirect(url_for('setting.index'))

@bp.route('/coin/<int:target_coin_id>/save', methods=('GET','POST'))
@login.login_required
def save_coin_setting(target_coin_id):
    if request.method=="POST":
        # Get Login User'DB Info
        login_userDB=web_tool.get_login_UserInfo(user_table="user_list",session_var=service.session_variable)

        # Get Request Form
        request_data={
            "market": request.form["market"], # required data
            "period": request.form["period"], # required data
            "strategy": request.form["strategy"], # required data
            "principal": request.form["principal"], # required data
            "bid_unit": request.form["bid_unit"],
            "bid_installment": request.form["bid_installment"],
            "ask_unit": request.form["ask_unit"],
            "ask_installment": request.form["ask_installment"],
            "target_earning": request.form["target_earning"],
            "loss_limit": request.form["loss_limit"],
            "auto_tunning": request.form["auto_tunning"],
            "alarm": request.form["alarm"],
            "mode": request.form["mode"],
            "is_tradingStop":False
        }

        # Request Data Check & Update Target Data
        if check_setting_req_Data(request_data)==False:
            return redirect(url_for('setting.set_coin', target_coin_id=target_coin_id))
        else: # Request Data is Ok
            target_setting_info = basic_tool.update_target_coin(
                origin_data=login_userDB[f"target_coin{target_coin_id}"],
                update_data=request_data)

        # Set Trading Data
        # save를 하게되면 trading관련 정보들은 모두 초기화
        if basic_tool.is_trading_run(request_data["mode"])==True:
            # (1) Mode Setting
            trading_state="Trading"
            # (2) Calc Start Time
            current_time_kst=basic_tool.get_current_kst_Time()
            start_time = current_time_kst

            # (3) Calc End Time
            set_days, set_hours, set_mins = read_setting_period(request_data["period"])

            trading_setting_time=basic_tool.calc_timeDelta(current_time_kst,
                                                           days=set_days,
                                                           hours=set_hours,
                                                           minutes=set_mins)

            end_time=trading_setting_time

        else:
            trading_state = "Ready"
            start_time=" - "
            end_time=" - "

        trading_data={
            "state":trading_state,
            "earning":"0",
            "earning_rate":"0%",
            "today_tradingNum":"0",
            "accum_tradingNum":"0",
            "start_time":start_time, # run or simulation을 설정한 시간
            "end_time":end_time,
            "stop_time":"",     # stop 버튼 누른 시간
            "restart_time":""   # restart 버튼 누른 시간    
        }

        # Trading Data Check & Update Target Data
        target_setting_info=basic_tool.update_target_coin(origin_data=target_setting_info, update_data=trading_data)

        # Update DB
        db = get_db()
        update_qry_cmd=f"UPDATE user_list SET target_coin{target_coin_id} = ? WHERE access_code = ?"
        update_data=(
            basic_tool.convert_dict_to_MySQLjson(target_setting_info),
            login_userDB["access_code"]
        )

        db.execute(update_qry_cmd, update_data)
        db.commit()

        return redirect(url_for('setting.index'))
    else:

        return redirect(url_for('setting.set_coin',target_coin_id=target_coin_id))
        # url_for 설정
        print("POST EORROR -> save_coin_setting(target_coin_id):")


@bp.route('/edit/<int:strategy_id>')
@login.login_required
def edit_strategy(strategy_id):
    # Strategy config정보가 있는 json 파일 업로드


    if strategy_id==1:
        strategy_info = STRATEGY1_CONFIG_DATA
    else:
        '''
        다른 strategy Info에 대해서는 설정 필요
        '''
        pass
    return render_template('setting/strategy_edit.html',strategy_id=strategy_id, strategy_info= strategy_info)


@bp.route('/save')
@login.login_required
def save_setting():
    login_userInfo=web_tool.session_get(session_var=service.session_variable)
    login_userEmail=login_userInfo["email"]
    server_db = get_db()
    db_table="user_list"

    login_userDB=web_tool.get_loginUserInfo(login_userEmail,server_db,db_table)

    return render_template('setting/setting.html',login_userDB=login_userDB)

