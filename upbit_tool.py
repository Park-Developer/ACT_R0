import pyupbit
import pandas
import numpy

ticker =pyupbit.get_tickers()
print(ticker)

# 과거 데이터 조회
df = pyupbit.get_ohlcv("KRW-BTC",)
print(df)
print("========================")
print(df["close"])
print("size",df["close"].shape[0])
print("========================")
print(df["close"][0])

def calc_movingAvg(period:int, count:int)->None:
    df = pyupbit.get_ohlcv("KRW-BTC",count=count)

    movingAvg_info=[None]*(count-period)

    close_df=df["close"] # 종가 추출




if __name__=="__main__":
    pass
