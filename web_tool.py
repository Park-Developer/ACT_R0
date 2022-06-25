import json
from flask import (
    session
)
import basic_tool
from Flask_Web.db import get_db


from werkzeug.security import check_password_hash, generate_password_hash



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


'''
def check_account(input_info:dict,check_data:dict)->bool: # 이거 다시 설장 # check data 바꾸기
    if check_data["data_type"]=="local_file": # local file로 비교하는 경우
        # user info loop
        with open(check_data["user_list_address"], 'r') as f1:
            user_list = json.load(f1)

        #with open(check_data["access_code_address"], 'r') as f2:
        #    access_code_list = json.load(f2)

        for email,user_info in user_list.items():
            if (input_info["email"]==email and input_info["password"]==user_info["PERSONAL_PART"]["password"]): # email & password check
                user_name=user_info["PERSONAL_PART"]["username"]

                access_code=user_info["TELEGRAM_PART"]["ACCESS_CODE"]["code"]
                code_generation_time=user_info["TELEGRAM_PART"]["ACCESS_CODE"]["generation_time"] # 코드 밟급 시간

                # 코드 일치 여부와 발급 시간으로 코드 유효성 평가하기
                code_lifetime=config.ACCOUNT_CHECK_METHOD["CODE_INFO"]["code_lifetime"]
                if(input_info["access_code"]==access_code and basic_tool.is_timeOver(code_generation_time,code_lifetime)==False):
                    return True
                else:
                    if input_info["access_code"]!=access_code:
                        print("입력 코드 불일치 에러")
                    elif basic_tool.is_timeOver(code_generation_time,code_lifetime)==True:
                        print("코드 생성시간 초과")

                    return False

        return False
    else: # ex) DB 비교
        pass
'''
if __name__ == '__main__':
    code_info = {
        "code_method": 0,
        "code_length": 8
    }

