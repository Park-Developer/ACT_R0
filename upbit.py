import pyupbit
import pandas
import numpy

ticker =pyupbit.get_tickers()
print(ticker)

# 현재 가격 조회
price=pyupbit.get_current_price("KRW-BTC")
print(price)

# 과거 데이터 조회
df = pyupbit.get_ohlcv("KRW-BTC", interval="minute5")
print(df)

access_key='InJd0c63bEGg8TE2lC16vuruckFNEFhMwBFVdYxC'
secret_key='P8yLpw2CcKPuwipLexYOXTfowgJ3mqcMCmsxkxfO'

upbit=pyupbit.Upbit(access_key,secret_key)
print(upbit.get_balances())
