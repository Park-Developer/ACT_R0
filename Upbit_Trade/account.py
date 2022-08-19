import jwt
import hashlib
import os
import requests
import uuid
from urllib.parse import urlencode, unquote
import Upbit_Trade.config


def read_account_balance(secret_key,access_key):
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
        'Authorization': authorization,
    }
    res = requests.get(Upbit_Trade.config.SERVER_URL + '/v1/accounts', headers=headers)

    account_info={}
    account_info["target_coin_list"]=[]
    account_info["target_coin_number"]=0

    # Data Load
    for idx,coin in enumerate(res.json()):
        if coin["currency"]=="KRW": # 보유하고 있는 원화
            account_info["KRW_balance"]=coin["balance"]
        else:
            account_info["target_coin_number"]+=1
            account_info["target_coin_list"].append(coin["currency"])

            account_info[coin["currency"]]=coin # 코인정보 기록 Ex) WAVES : {'currency': 'WAVES', 'balance': '1.0', 'locked': '0.0', 'avg_buy_price': '6310', 'avg_buy_price_modified': False, 'unit_currency': 'KRW'}

    return account_info

if __name__ == "__main__":
    access_key = "InJd0c63bEGg8TE2lC16vuruckFNEFhMwBFVdYxC"
    secret_key = "P8yLpw2CcKPuwipLexYOXTfowgJ3mqcMCmsxkxfO"

    print(read_account_balance(secret_key, access_key))