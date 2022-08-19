
import requests

url = "https://api.upbit.com/v1/candles/minutes/1?market=KRW-BTC&to=2022-08-01 00:00:00&count=60"

headers = {"Accept": "application/json"}

response = requests.get(url, headers=headers)

result=response.json()

for rs in result:
    print(rs)