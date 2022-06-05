import logging
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler
# This part is for setting up logging module
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# You have ot create an Application object.
application = ApplicationBuilder().token('1395535281:AAF2bNWr5YVhPhMreL-PU58qEQMx-BF-IYE').build()

# This application alone doesn't do anything. To add functionality, we do two things.
# First, we define a function that should process a specific type of updates
async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )


if __name__ == '__main__':
    application = ApplicationBuilder().token('TOKEN').build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()