import asyncio
import telegram
import json

with open('./user_config.json', 'r') as f:
    USER_INFO=json.load(f)
    print(USER_INFO["TELEGRAM_PART"]["TELEGRAM_API"])





#bot = telegram.Bot(token=api_key)
#bot.send_message(chat_id=user_id, text='USP-Python has started up!')