import pyupbit
import pandas
import numpy
import config

def get_balanceInfo(upbit_key:dict)->tuple:
    access_key=upbit_key["access_key"]
    secret_key=upbit_key["secret_key"]

    upbit=pyupbit.Upbit(access_key,secret_key)
    balance=upbit.get_balances()

    if balance==[]: # 계좌에 아무것도 없는 경우
        print("Nothing balance!")
        return {}


    cash_info=balance[0]    # 보유한 현금 정보(dict)
    coin_info=balance[1:]   # 보유한 코인 정보(list)

    return cash_info, coin_info # dict, list

if __name__=="__main__":
    upbit_key={
        "access_key":config.UPBIT_ACCESS_KEY,
        "secret_key":config.UPBIT_SECRET_KEY
    }

    a,b=get_balanceInfo(upbit_key)
    print(a)
    print(b)