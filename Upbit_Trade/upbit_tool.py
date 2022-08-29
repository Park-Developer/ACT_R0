import pandas
import pyupbit
import math
import requests
import uuid
import jwt

import Upbit_Trade.config
import Upbit_Trade.calc_tool

def get_UPBIT_coinInfo(caution_note=False)->list:
    if caution_note==False:
        url = "https://api.upbit.com/v1/market/all?isDetails=false"
    else:
        url = "https://api.upbit.com/v1/market/all?isDetails=true"

    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)

    result = response.json()

    return result

def get_UPBIT_marketlist(warning_filter=True)->list:
    if warning_filter==False:
        url = "https://api.upbit.com/v1/market/all?isDetails=false"
    else:
        url = "https://api.upbit.com/v1/market/all?isDetails=true"

    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    result = response.json()

    market_list=[]

    checked_market_list=list(Upbit_Trade.config.MARKET_CURRENCY_MATCHING.keys())
    '''
    Upbit_Trade.config.MARKET_CURRENCY_MATCHING에서 정의한 코인만 설정
    '''

    for coin_info in result:
        if coin_info["market"] in checked_market_list:
            if warning_filter==True:
                if coin_info["market_warning"]=="NONE":
                    market_list.append(coin_info["market"])
            else:
                market_list.append(coin_info["market"])

    return market_list

def get_current_coinInfo(market:str): # Ex) KRW-WAVES
    url = f"https://api.upbit.com/v1/ticker?markets={market}"

    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)

    result = response.json()[0]

    return result

def get_current_price(market:str): # Ex) KRW-WAVES
    coin_info=get_current_coinInfo(market)

    return int(coin_info["trade_price"])

def request_current_coinInfo(market:str): # Ex) KRW-WAVES
    url = f"https://api.upbit.com/v1/ticker?markets={market}"

    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)

    result = response.json()[0]

    return result

def request_current_price(market:str): # Ex) KRW-WAVES
    coin_info=request_current_coinInfo(market)

    return int(coin_info["trade_price"])


def convert_tick_to_currency():
    pass

def get_balanceInfo(access_key,secret_key)->list:
    server_url=Upbit_Trade.config.SERVER_URL
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
        'Authorization': authorization,
    }

    res = requests.get(server_url + '/v1/accounts', headers=headers)

    return res.json()

def get_KRW_balance(access_key,secret_key)->str:
    balance_info=get_balanceInfo(access_key,secret_key)

    return balance_info[0]["balance"]

def convert_market_to_currency(market:str)->str:
    try:
        result=Upbit_Trade.config.MARKET_CURRENCY_MATCHING[market]
    except KeyError:
        print("Upbit_Trade.config.MARKET_CURRENCY_MATCHING KEY ERROR!")
        result=None

    return result

def get_coin_balanceInfo(access_key,secret_key,market):
    balance_info = get_balanceInfo(access_key, secret_key)
    print(" get_coin_balanceInfo")
    for coin_info in balance_info:
        print("coin infoi",coin_info)
        if coin_info["currency"]==convert_market_to_currency(market):
            return coin_info

    return {}

def get_coin_balance(access_key,secret_key,market):
    # 현재 보유하고 있는 코인 개수 반환
    coin_info=get_coin_balanceInfo(access_key,secret_key,market)

    return int(coin_info["balance"])


def get_API_expireDate(access_key,secret_key):
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
        'Authorization': authorization,
    }

    res = requests.get(Upbit_Trade.config.SERVER_URL + '/v1/api_keys', headers=headers)
    result=res.json()

    return result[0]["expire_at"]

def get_past_Minutes_coinData(market:str,count:int,minute_unit=1,to:str=""):
    if to=="":
        url = f"https://api.upbit.com/v1/candles/minutes/{minute_unit}?market={market}&count={count}"
    else:
        url = f"https://api.upbit.com/v1/candles/minutes/{minute_unit}?market={market}&to={to}&count={count}"

    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    res_data=response.json()

    return res_data

def get_past_Days_coinData(market:str,count:int,to:str=""):
    if to=="":
        url = f"https://api.upbit.com/v1/candles/days?market={market}&count={count}"
    else:
        url = f"https://api.upbit.com/v1/candles/days?market={market}&to={to}&count={count}"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    res_data=response.json()

    return res_data

def get_past_Week_coinData(market:str,count:int,to:str=""):
    if to=="":
        url = f"https://api.upbit.com/v1/candles/weeks?market={market}&count={count}"
    else:
        url = f"https://api.upbit.com/v1/candles/weeks?market={market}&to={to}&count={count}"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    res_data=response.json()

    return res_data

def get_past_Month_coinData(market:str,count:int,to:str=""):
    if to=="":
        url = f"https://api.upbit.com/v1/candles/months?market={market}&count={count}"
    else:
        url = f"https://api.upbit.com/v1/candles/months?market={market}&to={to}&count={count}"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    res_data=response.json()

    return res_data

def get_past_coinData(market:str,count:int,data_unit:int,to:str=""):


    if data_unit >= 60*24*7*30: # Unit : Month
        past_data = get_past_Month_coinData(market=market, count=count, to=to)
    elif data_unit >= 60*24*7: # Unit : Week
        past_data = get_past_Week_coinData(market=market, count=count, to=to)
    elif data_unit >= 60*24: # Unit : Day
        past_data = get_past_Days_coinData(market=market, count=count, to=to)
    else:
        past_data = get_past_Minutes_coinData(market, count, minute_unit=data_unit, to=to)

    return past_data

def convert_pastData_to_Dict(market:str,count:int,data_unit:str,to:str="")->dict:
    past_data=get_past_coinData(market,count,data_unit,to) # list

    opening_price=[]
    high_price=[]
    low_price=[]
    trade_price=[]
    timestamp=[]
    candle_date_time_kst=[]

    for data in past_data:
        opening_price.append(float(data["opening_price"]))
        high_price.append(float(data["high_price"]))
        low_price.append(float(data["low_price"]))
        trade_price.append(float(data["trade_price"]))
        timestamp.append(data["timestamp"])
        candle_date_time_kst.append(data["candle_date_time_kst"])

    # 최신순으로 데이터가 모아지므로 과거데이터부터 받고 싶으면 순서를 뒤집어야함
    opening_price.reverse()
    high_price.reverse()
    low_price.reverse()
    trade_price.reverse()
    timestamp.reverse()
    candle_date_time_kst.reverse()

    converted_past_data={
        "opening_price":opening_price,
        "high_price":high_price,
        "low_price":low_price,
        "trade_price":trade_price,
        "timestamp":timestamp,
        "candle_date_time_kst":candle_date_time_kst
    }

    return converted_past_data

def calc_minute_closeAvg(market,minute_unit,past_data_count):
    '''
    past_data_count분 동안의 종가의 평균 계산
    (unit : minute_unit min)
    :return:
    '''

    res_data=Upbit_Trade.upbit_tool.get_past_Minutes_coinData(minute_unit,
                                                          market,
                                                          past_data_count)

    close_dataList=[]
    for data in res_data:
        close_dataList.append(data["trade_price"]) # trade_price : 종가

    return Upbit_Trade.calc_tool.calc_avg(close_dataList)

if __name__=="__main__":

    access_key = "InJd0c63bEGg8TE2lC16vuruckFNEFhMwBFVdYxC"

    secret_key = "P8yLpw2CcKPuwipLexYOXTfowgJ3mqcMCmsxkxfO"
