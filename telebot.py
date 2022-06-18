import logging
import logging
from telegram import Update,Bot
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler
# This part is for setting up logging module
import bot_cmd
import config
import web_tool
import basic_tool
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# You have ot create an Application object.
application = ApplicationBuilder().token('1395535281:AAF2bNWr5YVhPhMreL-PU58qEQMx-BF-IYE').build()

# This application alone doesn't do anything. To add functionality, we do two things.
# First, we define a function that should process a specific type of updates
async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    print("user_ud",update.effective_chat.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )

'''----------------------------------------------------------
USER-DEFINE COMMAND
----------------------------------------------------------'''
# ACT_Check
async def ACT_Check(update: Update, context: CallbackContext.DEFAULT_TYPE):
    target_coinInfo, user_tradeInfo=bot_cmd.ACT_Check(config.BOT_INFO)

    # [1] Message Line about ticker Info
    ticker_info_ln0 = '*[Target Coin List & Current Price(KRW)]*'  # Any characters between ** will be send in bold format.
    ticker_info_ln1=''

    for name,curVal in target_coinInfo.items():
        ticker_info_ln1=ticker_info_ln1+' - '+name+' : '+str(curVal)+"\n"

    # [2] User Trade Info
    user_info_ln0='*[User Trade State]*'
    def balance_examine(balance_info):
        if balance_info==[]:
            return "0";

    user_info_ln1=" - 잔액 : " + balance_examine(user_tradeInfo['잔액'])

    # [3] Message Setting
    check_msg=ticker_info_ln0+'\n'+ticker_info_ln1+"\n\n"+user_info_ln0+"\n"+user_info_ln1

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
    
        text=check_msg,
        parse_mode='Markdown'
    )

# Web Login CMD
async def ACT_Web_Login(update: Update, context: CallbackContext.DEFAULT_TYPE): # 수정필
    print("args",context.args,type(context.args))
    if len(context.args)==0: # args가 없는 경우
        print("asd",context.args)
        login_msg="HELDASD"#"Invalid command format\nPlease command in the following format\n\nACT_Web_Login email@ACT_R0.com"
    else:
        user_email = context.args[0] # input user email

        # Access Code 생성
        is_accessible, code, user_name=bot_cmd.ACT_Web_Login(user_email)

        if is_accessible == True:
            user_list_addr=config.ACCOUNT_CHECK_METHOD["USER_LIST_ADDRESS"]

            basic_tool.update_loginCode(code,user_email,user_list_addr) # Access Code Update

            login_msg = "Hello "+ user_name +"! \n\n*code* : " + code
        else:
            login_msg = code # error code

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=login_msg,
        parse_mode='Markdown'
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TELEGRAM_API).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # User Defined CMD
    check_handler = CommandHandler('ACT_Check', ACT_Check)
    application.add_handler(check_handler)

    web_login_handler = CommandHandler('ACT_Web_Login', ACT_Web_Login)
    application.add_handler(web_login_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()