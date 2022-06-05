import json
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler

# USER INFO SETTING
with open('./user_config.json', 'r') as f:
    USER_INFO=json.load(f)
    print(json.dumps(USER_INFO["TELEGRAM_PART"]["TELEGRAM_API"]))

TELEGRAM_BOT_API=json.dumps(USER_INFO["TELEGRAM_PART"]["TELEGRAM_API"])

# This part is for setting up logging module
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# This application alone doesn't do anything. To add functionality, we do two things.
# First, we define a function that should process a specific type of updates
async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_API).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler) # register command in the application

    application.run_polling()