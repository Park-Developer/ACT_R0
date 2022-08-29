import random

import config
import json
import time
import upbit_tool
from datetime import datetime, timedelta
import Upbit_Trade.Strategy1

def is_trading_Timeover(end_time:str):
    # (1) Calc End Time Timestamp
    end_time = datetime.strptime(end_time, config.TIME_FORMAT)
    end_time_timestamp = datetime.timestamp(end_time)

    # (2) Calc Current Time Timestamp
    cur_KST_time_str=get_current_kst_Time() # 문자열로 현재시간 받기
    cur_time=datetime.strptime(cur_KST_time_str,config.TIME_FORMAT) # 계산을 위해 tim형e으로 변환
    cur_time_timestamp=datetime.timestamp(cur_time)

    if (end_time_timestamp-cur_time_timestamp)>0:
        return False
    else:
        return True

def get_trading_state(trading_mode:str,end_time:str,is_tradingStop:bool):
    # trading state : Ready,Trading,Stop,Idle. End
    # trading mode : Ready, Run, Simulation, Idle(설정안한 경우)
    if trading_mode=="Ready":
        return "Ready"
    elif trading_mode=="Run" or trading_mode=="Simulation":
        if is_tradingStop==True or is_tradingStop=="True":
            return "Stop"
        else:
            if is_trading_Timeover(end_time) == False:
                return "Trading"
            else:
                return "End"

    elif trading_mode=="Idle":
        return "Idle"


def is_trading_run(mode_data):
    if (mode_data == "Run") or (mode_data == "run") or (mode_data == "Simulation") or (mode_data == "simulation"):
        return True
    else:
        return False

def calc_timeDelta(reference_time: str, days:int, hours:int, minutes:int) -> str:
    calced_time = datetime.strptime(reference_time, config.TIME_FORMAT) + timedelta(days=days,
                                                                             minutes=minutes,
                                                                             hours=hours)

    return calced_time.strftime(config.TIME_FORMAT)

def calc_timeGap(start_time: str, end_time: str) -> str:
    time_1 = datetime.strptime(start_time, config.TIME_FORMAT)
    time_2 = datetime.strptime(end_time, config.TIME_FORMAT)

    time_interval = time_2 - time_1

    hour_gap, min_gap = divmod(time_interval.seconds, 3600)

    time_gap = {
        "days": time_interval.days,
        "hour": hour_gap,
        "min": min_gap // 60
    }

    return time_gap

def clean_strData(str_data: str):
    v1 = str_data.replace('"', "")
    v2 = v1.replace("'", "")
    v3 = v2.replace(" ", "")

    return v3

def convert_MySQLjson_to_Dict(sql_data: str) -> dict:
    # Convert Mysql JSON to Python Dict
    v1 = sql_data.replace("{", "")
    v2 = v1.replace("}", "")
    v3 = v2.replace(" ", "")

    return read_target_stringInfo(v3)


def convert_dict_to_MySQLjson(dict_data:dict)->str:
    data_list=[]
    for key,value in dict_data.items():
        store_form=f'"{key}" : "{value}"'
        data_list.append(store_form)

    result="'{"+f'{", ".join(data_list)}'+"}'"

    return result

def update_target_coin(origin_data:dict, update_data:dict)->dict:
    try:
        for key,value in update_data.items():
            origin_data[key]=value

    except KeyError:
        print("update_target_coin klet eERror!")
        return {}
    else:
        return origin_data

def read_target_stringInfo(data: str) -> dict:
    dict_converted = {}

    if check_target_coin_data(data)==True:
        data_list = data.split(",")

        for data in data_list:
            if data != "":
                data_format = data.split(":")

                dict_converted[clean_strData(data_format[0])] = clean_strData(data_format[1])

    return dict_converted

def update_stringInfo(origin_data: str, update_data: dict) -> str:
    origin_dict = read_target_stringInfo(origin_data)

    # Update Data
    for key, update_value in update_data.items():
        origin_dict[key] = update_value

    # Convert to String
    result = []

    for key, value in origin_dict.items():
        result.append(key + ":" + value)  # 연결자 => :

    return ",".join(result)  # 연결자 => ,

def check_target_coin_data(data:str)->bool:

    if data=="1" or data==1:
        return False

    if data!="" and ":" in data:
        return True
    else:
        return False

def get_current_kst_Time():
    now_time = datetime.now().strftime(config.TIME_FORMAT) # TIME_FORMAT="%Y-%m-%d %H:%M:%S"

    # datetime 값으로 변환
    utc_time_format = datetime.strptime(now_time,config.TIME_FORMAT)

    # KST 시간을 구하기 위해 +9시간
    kst_time_format = utc_time_format #+ timedelta(hours=9)

    # 일자 + 시간 문자열로 변환
    return kst_time_format.strftime(config.TIME_FORMAT)

def is_timeOver(generation_time:str, code_lifetime:int)->bool:   # format : "2022-06-12 02:04:46"
    # [today time info]
    today_year = time.localtime().tm_year
    today_mon = time.localtime().tm_mon
    today_day = time.localtime().tm_mday
    today_hour = time.localtime().tm_hour
    today_min = time.localtime().tm_min
    today_sec = time.localtime().tm_sec

    # [date Check]
    record_date = generation_time.split(' ')[0]

    date_year=int(record_date.split('-')[0])
    date_mon=int(record_date.split('-')[1])
    date_day=int(record_date.split('-')[2])

    # 연도, 월, 일이 다르면 Over로 판단
    if(today_year!=date_year or today_mon!=date_mon or today_day!=date_day):
        return True

    # [time Check]
    record_time = generation_time.split(' ')[1]

    time_hour = int(record_time.split(":")[0]) # Hour
    time_min = int(record_time.split(":")[1])  # Min
    time_sec = int(record_time.split(":")[2])  # Sec

    # 시간이 다르면 Over로 판단
    if time_hour!=today_hour:

        return True
    else:
        record_info_SEC = (time_min*60) + (time_sec)
        today_info_SEC=(today_min*60) + (today_sec)

        if (today_info_SEC-record_info_SEC)> code_lifetime:
            return True
        else:
            return False

def check_username(userlist_addr:str,user_email:str)->str: # email로 user가 있는지 확인
    with open(userlist_addr, 'r') as f:
        user_list = json.load(f)

    if user_email in user_list: # email 검색
        print("check username")
        return True, user_list[user_email]["PERSONAL_PART"]["username"]
    else:
        return False, "Not Exist User"


def get_static_userInfo(email:str,data_addr:str,read_method:str)->dict:
    if read_method=="JSON": # json파일에서 정보 가져오기
        with open(data_addr, 'r') as f:
            user_list = json.load(f)

        static_info=user_list[email]

        return static_info

    else:
        print("Not Yet - get_static_userInfo")
        pass


def get_dynamic_userInfo(email:str,data_addr:str,read_method:str)->dict:
    if read_method == "JSON":  # json파일에서 정보 가져오기
        with open(data_addr, 'r') as f:
            user_list = json.load(f)

        static_info = user_list[email]
    else:
        print("Not Yet - get_dynamic_userInfo")

    access_key=static_info["UPBIT_PART"]["ACCESS_KEY"]
    secret_key = static_info["UPBIT_PART"]["SECRET_KEY"]

    cash_info, coin_info= upbit_tool.get_balanceInfo(access_key, secret_key)

    dynamic_info = {}

    dynamic_info["UPDATE_TIME"]=time.strftime('%Y-%m-%d %H:%M:%S') # update time record
    dynamic_info["CURRENT_CASH_BALANCE"]=cash_info  # 보유한 현금 정보(dict)
    dynamic_info["CURRENT_COIN_LIST"]=coin_info  # 보유한 코인 정보(list)

    return dynamic_info

def get_userInfo(email:str,data_addr:str,read_method:str)->dict:
    # user info = static user info + dynamic user info

    # (1) Get Static User Info
    user_info=get_static_userInfo(email,data_addr,read_method)

    # (2) Update Dynamic User Info
    user_info["DYNAMIC_PART"]=get_dynamic_userInfo(email,data_addr,read_method)

    return user_info


def update_loginCode(code:str,user_email:str,user_list_addr:str)->None:
    # (1) read access code list
    with open(user_list_addr, 'r') as f:
        user_list = json.load(f)

    # (2) reset code with lifetime

    ''' # 유효성 평가 작업
    for user_email,user_info in user_list.items():
        # JSON format check
        if ("code" in code_info and "generation_time" in code_info):
            generation_time=code_info["generation_time"]
            if is_timeOver(generation_time,code_lifetime)==True: # lifetime을 초과한 경우
                life_end_list.append(user_name)

    for user_name in life_end_list:
        del access_code_list[user_name] # 해당 username 삭제
    '''

    # (3) update access code & JSON update
    user_list[user_email]["TELEGRAM_PART"]["ACCESS_CODE"]["code"]=code
    user_list[user_email]["TELEGRAM_PART"]["ACCESS_CODE"]["generation_time"]=time.strftime('%Y-%m-%d %H:%M:%S')

    with open(user_list_addr, 'w') as f:
        json.dump(user_list_addr, f,indent=2)


def gen_loginCode(code_info: dict) -> str:
    '''
    Code Generator
    - 8자리의 숫자+영어(대문자) 조합
    - code_method : 코드를 생성하는 방법(0:default)
    '''

    if (code_info["code_method"] == 0):

        result = ""
        for i in range(code_info["code_length"]):
            int_or_char = random.randrange(0, 2)

            if int_or_char == 0:  # 숫자 선택
                code = str(random.randrange(0, 10))  # 0부터 9까지의 정수 반환
            else:  # 문자 선택
                code = chr(random.randrange(65, 91))  # 65(A)부터 90(Z)까지의 아스키코드 반환

            result = result + code

        return result
    else:
        pass  # 다른 방법


def get_strategy_configData(target_coin_id:int, login_userDB):
    # Get UPBIT API Info
    upbit_apiInfo = {
        "upbit_access_key": login_userDB["upbit_access_key"],
        "upbit_secret_key": login_userDB["upbit_secret_key"]
    }

    # Get Target Coin Info
    target_coinInfo=login_userDB[f"target_coin{target_coin_id}"]

    return upbit_apiInfo, target_coinInfo

def get_strategy_clsObj(target_coinInfo):
    if target_coinInfo["strategy"] == "Strategy1":
        strategy_obj = Upbit_Trade.Strategy1.Strategy()
    else:
        pass

    return strategy_obj

# 이거 지워도 될듯?
def get_trading_strategy_Obj(target_coin_id:int, login_userDB):
    # Get UPBIT API Info
    upbit_apiInfo={
        "upbit_access_key":login_userDB["upbit_access_key"],
        "upbit_secret_key":login_userDB["upbit_secret_key"]
    }

    # Get Target Coin Info
    target_coinInfo=login_userDB[f"target_coin{target_coin_id}"]

    # Create Trading_Config Class Obj
    Trading_config=Upbit_Trade.Trading_Config()

    # Crate UpbitTrade.Strategy Cls Obj
    if target_coin_id==1:
        strategy_obj =Upbit_Trade.Strategy1.Strategy()
    else:
        pass

    # Load Data
    strategy_obj.load_configData(upbit_apiInfo=upbit_apiInfo,
                            target_coinInfo=target_coinInfo)


    return strategy_obj



if __name__ == '__main__':
    pass
