import pyupbit
import pandas
import numpy
import config
'''
[Command Lists]
- ACT_Start : 자동 매매 프로그램 시작(매수 - 매도 시작)
- ACT_End : 자동 매매 프로그램 중지
- ACT_Check : 현황 조회
- ACT_Modi : ACT 설정 변경
- ACT_Sim : Simulation 모드로 변경
- ACT_Real : 실제 매매 모드로 변경
- ACT_Monitoring
- ACT_Log
'''

def ACT_Start():
    pass
def ACT_End():
    pass
def ACT_Check(bot_info:dict)->tuple:
    '''
    현재 현황을 조회하는 기능
    :return: target_coinInfo, user_tradeInfo
    '''
    target_list = bot_info["UPBIT_PART"]["TARGET_COIN"].split(',')
    access_key=bot_info["UPBIT_PART"]["ACCESS_KEY"]
    secret_key=bot_info["UPBIT_PART"]["SECRET_KEY"]

    target_coinInfo={} # 타겟 코인에 대한 정보 Dict
    user_tradeInfo={}  # User의 거래 현황

    # [1] Target Coin 정보
    for coin_ticker in target_list:
        coin_name=config.coin_ticker[coin_ticker]
        coin_curCost=pyupbit.get_current_price(coin_ticker)

        target_coinInfo[coin_name]=coin_curCost

    # [2] Target Coin의 현재가격 출력
    balance=pyupbit.Upbit(access_key,secret_key).get_balances()
    user_tradeInfo["잔액"]=balance

    return target_coinInfo, user_tradeInfo

def ACT_Modi():
    pass
def ACT_Sim():
    pass
def ACT_Real():
    pass

# TEST CODE
if __name__=="__main__":
    import asyncio
    import telegram
    import json

    with open('./user_config.json', 'r') as f:
        BOT_INFO = json.load(f)

    print(ACT_Check(BOT_INFO)[1])
