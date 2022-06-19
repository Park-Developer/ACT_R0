import json

# [SYSTEM SETTING]
ACT_MODE = "development" # 개발(관리자) 모드

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
    "USER_LIST_ADDRESS":"./user_list.json",
    "CHECK_DATA_TYPE":"local_file", # account 확인하는 방법
    "CODE_INFO":{
        "code_method": 0,
        "code_length": 8,
        "code_lifetime":180, # Unit : sec
    },
    "SESSION_VARIABLE":"user_email"
}

if __name__=="__main__":
    print(BOT_INFO)
