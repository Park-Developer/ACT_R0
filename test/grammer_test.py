'''
record_time="2022-06-12 02:04:46"

data=record_time.split(' ')[0]
time=record_time.split(' ')[1]

time_hour=time.split(":")[0]
time_min=time.split(":")[1]
time_sec=time.split(":")[2]

time_info_SEC=(int(time_hour)*3600)+(int(time_min)*60)+int(time_sec)

print(time_hour)
print(time_min)
print(time_info_SEC)
'''

import time
today_year = time.localtime().tm_year
today_mon = time.localtime().tm_mon
today_day = time.localtime().tm_mday
today_hour = time.localtime().tm_hour
print(today_hour, type(today_day))