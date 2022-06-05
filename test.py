import asyncio
import telegram
import json

with open('./user_config.json', 'r') as f:
    USER_INFO=json.load(f)
    print(USER_INFO["TELEGRAM_PART"]["TELEGRAM_API"])
