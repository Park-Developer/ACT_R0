import pyupbit
import pandas
import numpy

def calc_average(coin_ticker:str, count:int)->int:
    # 종가기준 평균값 반환
    if count==0:
        print("ERROR!!")
        return -9999
    else:
        df = pyupbit.get_ohlcv(coin_ticker, count=count)
        close_df = df["close"]  # 종가 반환

        return sum(close_df.values)/count


def make_movingAvg(coin_ticker:str,period:int, count:int)->dict:
    '''
    :param period:이평선 계산 기준 Ex) 5 : 5일 이동평균선
    :param count: 전체 조사 기간
    :return: movingAvg_info
    '''
    df = pyupbit.get_ohlcv(coin_ticker,count=count) # 일(day)단위 과거 데이터 추출
    close_df = df["close"]  # 종가 추출

    movingAvg_info={} # 이평선 반환값

    for i in range(count-period+1):
        day=period-1+i
        movingAvg_info[str(close_df.index[day])]=sum(close_df.values[day-period+1:day+1])/period

    print("[Moving Average] => coin ticker : {0}, period : {1}, count : {2}".format(coin_ticker,period,count))

    return movingAvg_info


def get_balanceInfo(access_key:str, secret_key:str)->tuple:
    upbit=pyupbit.Upbit(access_key,secret_key)
    balance=upbit.get_balances()

    if balance==[]: # 계좌에 아무것도 없는 경우
        print("Nothing balance!")
        return {}


    cash_info=balance[0]    # 보유한 현금 정보(dict)
    coin_info=balance[1:]   # 보유한 코인 정보(list)

    return cash_info, coin_info # dict, list

if __name__=="__main__":

    # [1] 이동평균선
    print(make_movingAvg(coin_ticker="KRW-BTC",period=3,count=6))
