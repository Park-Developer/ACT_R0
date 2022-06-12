import pyupbit
coin_ticker="KRW-BTC"
period=3
count=2

df = pyupbit.get_ohlcv(coin_ticker,count=count)
close_df=df["close"] # 종가 반환
print(sum(close_df.values))

def calc_Integration(time_unit:float,monitoring_number:int,data_list:list):

    if monitoring_number==0:
        print("abnormal monitoring number Error!")
        return {}
    else:
        average=sum(data_list)/monitoring_number # 평균 계산
        min_val=min(data_list)
        max_val=max(data_list)

        plus_area=0
        minus_area=0

        criteria=(max_val-min_val)/2

        for data in data_list:
            if data>=criteria:
                plus_area=plus_area+(data-criteria)*time_unit
            else:
                minus_area = minus_area + abs(data-criteria)*time_unit

        ratio = (plus_area/minus_area)*100

        area_info={
            "ratio":ratio,
            "criteria":criteria,
            "average":average,
            "plus_area":plus_area,
            "minus_area":minus_area,
            "min":min_val,
            "max":max_val,
        }

        return area_info

if __name__=="__main__":
    time_unit=1.2
    monitoring_number=10
    data_list=[29,23,5,7,1,2,2,44,11,22]
    result1=calc_Integration(time_unit ,monitoring_number, data_list)
    print(result1)

