import jwt
import hashlib
import os
import requests
import uuid
from urllib.parse import urlencode, unquote
import Upbit_Trade.config
import Upbit_Trade.Strategy1.strategy1

access_key = "InJd0c63bEGg8TE2lC16vuruckFNEFhMwBFVdYxC"
secret_key = "P8yLpw2CcKPuwipLexYOXTfowgJ3mqcMCmsxkxfO"
server_url = "https://api.upbit.com"

'''
개발을 위해 KRW-WAVES로 테스트
'''
if __name__=="__main__":

    upbit_apiInfo={
        "upbit_access_key":access_key,
        "upbit_secret_key":secret_key
    }

    target_coinInfo={
        "market":"KRW-WAVES",
        "period":"1Hour",
        "strategy":"Strategy1",
        "principal":"100000",
        "bid_unit":"50000",
        "bid_installment":"1",
        "ask_unit":"50000",
        "ask_installment":"1",
        "target_earning":"5%",
        "loss_limit":"-5%",
        "alarm":"None",
        "state":"Simulation",
        "balance":"1",
        "avg_buy_price":"6310",
        "cur_price":"8065.0",
        "earning":"0",
        "earning_rate":"0%",
        "today_tradingNum":"0",
        "accum_tradingNum":"0",
        "start_time":"2022-08-11-09-59-04",
        "end_time":"2022-08-11-10-59-04",
        "remain_time":"Days--1-Hours-23-Minutes-32"
    }

    strgy_cls=Upbit_Trade.Strategy1.strategy1.Strategy(test_cls)

    print("Current Price : ", Upbit_Trade.upbit_tool.get_current_price(strgy_cls.coin_info.market))
    print("------------[ TEST CASE1 ]------------ ")
    print("strgy_cls.calc_ref_price()")
    print(strgy_cls.calc_ref_price())

    print("------------[ TEST CASE2 ]------------ ")
    print("strgy_cls.calc_Bid_max_Price()")
    print(strgy_cls.calc_Bid_max_Price())

    print("------------[ TEST CASE3 ]------------ ")
    print("strgy_cls.calc_Ask_min_Price()")
    print(strgy_cls.calc_Ask_min_Price())

    print("------------[ TEST CASE4 ]------------ ")
    print("strgy_cls.check_bid_timing()")
    print(strgy_cls.check_bid_timing())

    print("------------[ TEST CASE5 ]------------ ")
    print("strgy_cls.check_ask_timing()")
    print(strgy_cls.check_ask_timing())

    print("------------[ TEST CASE6 ]------------ ")
    print("bid()")

    print(strgy_cls.coin_info.bid(strgy_cls.check_bid_timing,strgy_cls.calc_Bid_max_Price()))
    print("strgy_cls.coin_info.KRW_balance", strgy_cls.coin_info.KRW_balance)
    print("strgy_cls.coin_info.coin_balance", strgy_cls.coin_info.coin_balance)
    print("------------ TEST END ------------ ")
