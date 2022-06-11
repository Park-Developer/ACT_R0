import random
import config
import json
import time


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

def check_username(userlist_addr:str,user_email:str)->str:
    with open(userlist_addr, 'r') as f:
        user_list = json.load(f)

    print("user list ", user_list)

    if user_email in user_list:
        print("check username")
        return True, user_list[user_email]["username"]
    else:
        return False, "Not Exist User"


def update_loginCode(code_addr:str,code_lifetime:int,user:str,code:str)->None:
    # (1) read access code list
    with open(code_addr, 'r') as f:
        access_code_list = json.load(f)

    # (2) reset code with lifetime
    life_end_list=[]
    for user_name,code_info in access_code_list.items():
        # JSON format check
        if ("code" in code_info and "generation_time" in code_info):
            generation_time=code_info["generation_time"]
            if is_timeOver(generation_time,code_lifetime)==True: # lifetime을 초과한 경우
                life_end_list.append(user_name)

    for user_name in life_end_list:
        del access_code_list[user_name] # 해당 username 삭제

    # (3) write code
    access_code_list["UPDATE_INFO"]=time.strftime('%Y-%m-%d %H:%M:%S') # 파일 수정 정보 기록

    access_code_list[user] = {
        "code":code,
        "generation_time":time.strftime('%Y-%m-%d %H:%M:%S')
    }

    with open(code_addr, 'w') as f:
        json.dump(access_code_list, f,indent=2)


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



if __name__ == '__main__':
    code_info = {
        "code_method": 0,
        "code_length": 8
    }

