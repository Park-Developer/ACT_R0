import json

# COIN INFORMATION
coin_ticker={   # coin ticker : coin name
    "KRW-ADA":"에이다",
    "KRW-SOL":"솔리나",
    "KRW-XRP":"리플",
    "KRW-WAVES":"웨이브",
}

# Config JSON File Load
with open('./user_config.json', 'r') as f:
    BOT_INFO = json.load(f)


TELEGRAM_API=BOT_INFO["TELEGRAM_PART"]["TELEGRAM_API"]

if __name__=="__main__":
    print(BOT_INFO)