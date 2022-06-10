import pyupbit
import pandas
import numpy

ticker =pyupbit.get_tickers()
print(ticker)

# 과거 데이터 조회
df = pyupbit.get_ohlcv("KRW-BTC",)

'''
print(df)asd
print("========================")
print(df["close"])
print("size",df["close"].shape[0])
print("========================")
print(df["close"][0])
'''

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

if __name__=="__main__":

    # [1] 이동평균선
    print(make_movingAvg(coin_ticker="KRW-BTC",period=3,count=6))
