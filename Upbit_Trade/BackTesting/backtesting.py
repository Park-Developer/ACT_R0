import Upbit_Trade.upbit_tool
import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def draw_plot(x,y):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()

def save_csvFile(data_list:dict):
    data_df = pd.DataFrame(data_list)
    data_df.to_csv('test.csv', index=False)

if __name__=="__main__":
    market = "KRW-WAVES"

    # [1] Get Day Data
    count = 60
    day_data = Upbit_Trade.upbit_tool.get_past_Days_coinData(market, count)
    day_price=[]
    day_time=[]
    for t in day_data:
        day_price.append(t["trade_price"])
        day_time.append(t["candle_date_time_kst"])

    day_datalist={
        "time":day_time,
        "price":day_price
    }

    # [2] Get Min Data
    count = 60
    min_data = Upbit_Trade.upbit_tool.get_past_Minutes_coinData(market, count)
    min_price=[]
    min_time=[]
    for t in min_data:
        min_price.append(t["trade_price"])
        min_time.append(t["candle_date_time_kst"])

    min_datalist={
        "time":min_time,
        "price":min_price
    }

    plt.plot(day_time,day_price,'g-',min_time,min_price,'r-')
    plt.show()