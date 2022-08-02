import json
import logging
import web_tool
from flask import render_template
from werkzeug.security import check_password_hash, generate_password_hash
import ACT_Error
import functools
from Flask_Web.db import get_db

# [SYSTEM GLOBAL VARIABLE SETTING]
CONFIG_JSON_ADDRESS="./config.json"
ACT_MODE = "development" # 개발(관리자) 모드
MASTER_MODE=False

# [LOGGER SETTING]
class CustomFormatter(logging.Formatter): # Handler 출력형식 지정
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(funcName)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Logger 설정
LOGGER_NAME="ACT_R0"

ACT_logger= logging.getLogger(LOGGER_NAME)
ACT_logger.setLevel(logging.DEBUG) # 로그의 출력 Level 설정

# Handler 설정
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(CustomFormatter())

# Handler 등록
ACT_logger.addHandler(stream_handler)

# log를 파일에 출력
#file_handler = logging.FileHandler('my.log')
#file_handler.setFormatter(formatter)
#logger.addHandler(file_handler)

# [CLASS DEFINITION]
class ACT_CONFIG: # SUPER CLASS
    def __init__(self):
        # Read config json file
        with open(CONFIG_JSON_ADDRESS, 'r') as f:
            self.ACT_info = json.load(f)

        if self.ACT_info["DEBUG_MODE"]==True: # (1) DEBUG MODE
            self.DEBUG_MODE = True
            ACT_logger.info("DEBUG MODE")
        else:                                 # (2) SERVER MODE
            self.DEBUG_MODE = False
            ACT_logger.info("SERVER MODE")

    def show_config(self): # => overload 필요
        print("ACT CONFIG")


class Master(ACT_CONFIG): # CHIlD1 CLASS
    def __init__(self):
        super().__init__() # 부모 클래스 __init__호출
        self.Master_info=self.ACT_info["MASTER"]

        # CONSTANT VARIABLE => 형식 오류에 대한 에러처기 기능 추가
        # [1] Telegram Part
        self.TELEGRAM_API = self.Master_info["TELEGRAM_PART"]["TELEGRAM_API"]
        self.login_access_code=self.Master_info["TELEGRAM_PART"]["ACCESS_CODE"]["code"]
        self.login_access_codeTime=self.Master_info["TELEGRAM_PART"]["ACCESS_CODE"]["generation_time"]

        # [2] Personal Part
        self.USER_EMAIL = self.Master_info["PERSONAL_PART"]["email"]
        self.USER_PASSWORD = self.Master_info["PERSONAL_PART"]["password"]
        self.USER_NAME = self.Master_info["PERSONAL_PART"]["username"]

        self.USER_TIER=self.Master_info["PERSONAL_PART"]["tier"]
        self.LOGIN_STATE=self.Master_info["PERSONAL_PART"]["login_state"]
        self.PROGILE_IMG_ADDR=self.Master_info["PERSONAL_PART"]["profile_img_addr"]

        # [3] Upbit Part
        self.UPBIT_ACCESS_KEY = self.Master_info["UPBIT_PART"]["ACCESS_KEY"]
        self.UPBIT_SECRET_KEY = self.Master_info["UPBIT_PART"]["SECRET_KEY"]
        self.ALLOWED_IP = self.Master_info["UPBIT_PART"]["ALLOWED_IP"]
        self.TARGET_COIN = self.Master_info["UPBIT_PART"]["TARGET_COIN"]

        # [4] Volatile Part
        self.update_time=self.Master_info["VOLATILE_PART"]["UPDATE_TIME"]
        self.current_cash_balance=self.Master_info["VOLATILE_PART"]["CURRENT_CASH_BALANCE"]
        self.current_coin_list=self.Master_info["VOLATILE_PART"]["CURRENT_COIN_LIST"]

        # [5] Post Part
        if self.DEBUG_MODE == True: # debug mode인 경우
            self.write_post="2"
            self.view_post="1,2"
            self.like_post="1"
            self.dislike_post="2"
        else:
            self.write_post=self.Master_info["POST_PART"]["WRITE_POST"]
            self.view_post=self.Master_info["POST_PART"]["VIEW_POST"]
            self.like_post=self.Master_info["POST_PART"]["LIKE_POST"]
            self.dislike_post=self.Master_info["POST_PART"]["DISLIKE_POST"]

    def get_master_info(self):
        result=(
            self.USER_EMAIL,
            self.USER_NAME,
            generate_password_hash(self.USER_PASSWORD),
            self.USER_TIER,
            self.LOGIN_STATE,
            self.PROGILE_IMG_ADDR,
            self.TELEGRAM_API,
            self.login_access_code,
            self.login_access_codeTime,
            self.UPBIT_ACCESS_KEY,
            self.UPBIT_SECRET_KEY,
            self.ALLOWED_IP,
            self.TARGET_COIN,
            self.update_time,
            self.current_cash_balance,
            self.current_coin_list,
            self.write_post,
            self.view_post,
            self.like_post,
            self.dislike_post
        )

        return result

    def show_config(self): # => overload 필요
        print("MASTER CONFIG")
        print(self.Master_info)


class Service(ACT_CONFIG): # CHIlD1 CLASS
    def __init__(self):
        super().__init__() # 부모 클래스 __init__호출
        self.Servie_info=self.ACT_info["SERVICE"]

        try:
            # CONSTANT VARIABLE => 형식 오류에 대한 에러처기 기능 추가
            # [1] Access Code Part
            self.access_code_method=self.Servie_info["CODE_INFO"]["code_method"]
            self.access_code_length =self.Servie_info["CODE_INFO"]["code_length"]
            self.access_code_lifetime =self.Servie_info["CODE_INFO"]["code_lifetime"]

            self.session_variable=self.Servie_info["SESSION_VARIABLE"]
            self.data_info=self.Servie_info["CHECK_DATA_TYPE"]
        except  KeyError as key:
            ACT_logger.error("cfg_err : Config JSON Load Error")
        else:
            ACT_logger.debug("config json load success")
    def show_config(self): # => overload 필요
        print("SERVIVE CONFIG")
        print(self.Servie_info)




# [COIN INFORMATION]
COIN_TICKER={   # coin ticker : coin name
    "KRW-ADA":"에이다",
    "KRW-SOL":"솔리나",
    "KRW-XRP":"리플",
    "KRW-WAVES":"웨이브",
}

# [Config USER_INFO File(.JSON) Load]
with open('./user_config.json', 'r') as f: # 이거 없애기
    BOT_INFO = json.load(f)


TELEGRAM_API=BOT_INFO["TELEGRAM_PART"]["TELEGRAM_API"]

USER_EMAIL=BOT_INFO["PERSONAL_PART"]["email"]
USER_PASSWORD=BOT_INFO["PERSONAL_PART"]["password"]
USER_NAME=BOT_INFO["PERSONAL_PART"]["username"]

UPBIT_ACCESS_KEY=BOT_INFO["UPBIT_PART"]["ACCESS_KEY"]
UPBIT_SECRET_KEY=BOT_INFO["UPBIT_PART"]["SECRET_KEY"]

# [WEB INFORMATION]
ACCOUNT_CHECK_METHOD={
    "USER_LIST_ADDRESS":"./user_list.json", # DB로 바꿀꺼임
    "CHECK_DATA_TYPE":"local_file", # account 확인하는 방법
    "CODE_INFO":{
        "code_method": 0,
        "code_length": 8,
        "code_lifetime":180, # Unit : sec
    },
    "SESSION_VARIABLE":"user_email"
}



if __name__=="__main__":
    print("==========MASTER============")
    master= Master()
    master.show_config()

    print("==========SERVICE============")
    service= Service()
    service.show_config()
