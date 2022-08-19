import pyupbit
import pandas
import numpy


# 잔고 조회
access_key='InJd0c63bEGg8TE2lC16vuruckFNEFhMwBFVdYxC'
secret_key='P8yLpw2CcKPuwipLexYOXTfowgJ3mqcMCmsxkxfO'

upbit=pyupbit.Upbit(access_key,secret_key)
print(upbit.get_balances())
'''
최소주문금액 5000원임
'''

buy_price=684
buy_num=9
#ret=upbit.sell_limit_order("KRW-ADA",buy_price,buy_num)
#print(ret)


