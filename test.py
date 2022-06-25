import asyncio
import telegram
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)


#bot = telegram.Bot(token=api_key)
#bot.send_message(chat_id=user_id, text='USP-Python has started up!')