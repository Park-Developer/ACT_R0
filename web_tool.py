import json
from flask import (
    session
)
import basic_tool
from Flask_Web.db import get_db
from collections import defaultdict

from werkzeug.security import check_password_hash, generate_password_hash

import Upbit_Trade.account

import basic_tool

def session_update(session_var:str,session_data:dict)->None:
    session[session_var] = session_data

def session_get(session_var:str)->dict:
    return session.get(session_var)

def session_clear()->None:
    session.clear()

def get_login_username(session_var:str)->str:
    user_info=session_get(session_var)
    if user_info==None:
        username="ERROR!"
    else:
        username=user_info["username"]

    return username

def get_strategyInfo(strategy_name:str)->dict:
    # DB 데이터를 dict 데이터로 변환
    db = get_db()
    stratey_Info = dict(db.execute(f"SELECT * FROM strategy WHERE name = ?", (strategy_name,)).fetchone())

    return stratey_Info

def get_login_UserInfo(user_table,session_var):
    '''
    login user 정보를 access_code를 통해서 session에서 찾은 후, DB 데이터 반환
    :param user_table:
    :return:
    '''

    # [1] session으로부터 login user데이터 get
    login_userInfo=session_get(session_var)
    login_userAccessCode = login_userInfo["access_code"]

    # [2] DB에서 login User Data Read
    db = get_db()

    # DB 데이터를 dict 데이터로 변환
    user_Info = dict(db.execute(f"SELECT * FROM {user_table} WHERE access_code = ?", (login_userAccessCode,)).fetchone())

    # [3] UPBIT API로 정보 최신화
    user_UPBIT_secret_key=user_Info["upbit_secret_key"]
    user_UPBIT_access_key=user_Info["upbit_access_key"]

    UPBIT_info=Upbit_Trade.account.read_account_balance(secret_key=user_UPBIT_secret_key,
                                 access_key=user_UPBIT_access_key)

    # (3-1) 보유한 원화 현금 조회
    KRW_balance = UPBIT_info["KRW_balance"]

    # (3-2) Target Coin Data Update
    TARGET_COIN_MAX_NUMBER = 5 # cofig.json에서 5개로 정의

    current_time_kst = basic_tool.get_current_kst_Time()  # 현재 시간(KST)

    updated_target_data={
        "target_coin1": {},
        "target_coin2": {},
        "target_coin3": {},
        "target_coin4": {},
        "target_coin5": {}
    }

    for coin_idx in range(TARGET_COIN_MAX_NUMBER):

        if basic_tool.check_target_coin_data(user_Info[f"target_coin{coin_idx + 1}"])==True: # Normal Case

            # Convert Mysql JSON to Python Dict
            converted_target_data=basic_tool.convert_MySQLjson_to_Dict(user_Info[f"target_coin{coin_idx + 1}"])

            market=converted_target_data["market"]


            # Get Current Data Using UPBIT API
            coin_balance_info=Upbit_Trade.upbit_tool.get_coin_balanceInfo(user_UPBIT_access_key,
                                                                          user_UPBIT_secret_key,
                                                                          market)

            if coin_balance_info=={}:
                print("coin_balance_ERROR!!!!!")
                update_data = {
                    "balance": "Error",
                    "avg_buy_price": "Error",
                    "cur_price": "Error"
                }
            else:
                update_data={
                    "balance":coin_balance_info["balance"],
                    "avg_buy_price":coin_balance_info["avg_buy_price"],
                    "cur_price":Upbit_Trade.upbit_tool.get_current_price(market)
                }

            # Update Dict Data (updated_target_data는 업데이트가 된 dict 데이터)
            updated_target_data[f"target_coin{coin_idx + 1}"]=basic_tool.update_target_coin(
                                                        origin_data= converted_target_data,
                                                        update_data= update_data)

            # Update Time Data and Mode
            if "mode" in updated_target_data[f"target_coin{coin_idx + 1}"]: # setting 작업을 했는지 검사
                saved_mode=updated_target_data[f"target_coin{coin_idx + 1}"]["mode"]
                saved_endTime = updated_target_data[f"target_coin{coin_idx + 1}"]["end_time"]
                saved_is_tradingStop = updated_target_data[f"target_coin{coin_idx + 1}"]["is_tradingStop"]

                # (1) Trading State Update
                trading_state=basic_tool.get_trading_state(trading_mode=saved_mode,
                                                           end_time=saved_endTime,
                                                           is_tradingStop=saved_is_tradingStop)

                updated_target_data[f"target_coin{coin_idx + 1}"]["state"]=trading_state

        else:
            user_Info[f"target_coin{coin_idx + 1}"]={}


    account_update_cmd="UPDATE user_list SET target_coin1 = ?," \
                       "target_coin2 = ?," \
                       "target_coin3 = ?," \
                       "target_coin4 = ?," \
                       "target_coin5 = ?," \
                       "balance_update_time = ?,"\
                       "current_cash_balance = ?" \
                       " WHERE access_code = ?"

    update_data=(
        basic_tool.convert_dict_to_MySQLjson(updated_target_data["target_coin1"]), # update var
        basic_tool.convert_dict_to_MySQLjson(updated_target_data["target_coin2"]), # update var
        basic_tool.convert_dict_to_MySQLjson(updated_target_data["target_coin3"]), # update var
        basic_tool.convert_dict_to_MySQLjson(updated_target_data["target_coin4"]), # update var
        basic_tool.convert_dict_to_MySQLjson(updated_target_data["target_coin5"]), # update var

        current_time_kst,                         # update var
        KRW_balance,                      # update var

        user_Info["access_code"]          # where var
    )

    db.execute(account_update_cmd, update_data)
    db.commit()

    # Update된 DB 데이터 다시 불러오기 및 가공(For Jinja Template)
    user_Info_dict = dict(db.execute(f"SELECT * FROM {user_table} WHERE access_code = ?", (login_userAccessCode,)).fetchone())
    '''
    sql 객체의 경우 데이터 수정이 불가능하며, 수정하려고하면 하기 에러 발생 
    => dict 객체로 변환해준다.
    TypeError: 'sqlite3.Row' object does not support item assignment
    '''
    for coin_idx in range(TARGET_COIN_MAX_NUMBER):
        user_Info_dict[f"target_coin{coin_idx + 1}"]=basic_tool.convert_MySQLjson_to_Dict(user_Info_dict[f"target_coin{coin_idx + 1}"])

    return user_Info_dict


def set_loginState(is_login:bool,user_data_addr:str,login_user_name:str)->None:
    with open(user_data_addr, 'r') as f:
        user_list = json.load(f)

    for email,user_info in user_list.items():
        if user_info["username"]==login_user_name:
            if is_login==True:
                user_info["login_state"]="ON"
            else:
                user_info["login_state"] = "OFF"
            break

def check_account(db_table:str,user_input:dict,server_db)->bool: # code에 대한 검사는 빠져있음 ㅜ
    user_input__email=user_input["email"]
    user_input__pwd=user_input["password"]

    # Excute SQL
    user_db = server_db.execute(
        f'SELECT * FROM {db_table} WHERE email = ?', (user_input__email,)
    ).fetchone()

    error=None

    if user_db==None:
        error="Incorrect useremail"
    elif not check_password_hash(user_db['password'],user_input__pwd):
        error = 'Incorrect password.'

    if error== None:
        return True, user_db
    else:
        return False, {}

if __name__ == '__main__':
    code_info = {
        "code_method": 0,
        "code_length": 8
    }

