import jwt
import hashlib
import os
import requests
import uuid
from urllib.parse import urlencode, unquote

access_key = "InJd0c63bEGg8TE2lC16vuruckFNEFhMwBFVdYxC"
secret_key = "P8yLpw2CcKPuwipLexYOXTfowgJ3mqcMCmsxkxfO"
server_url = "https://api.upbit.com"

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key)
authorization = 'Bearer {}'.format(jwt_token)
headers = {
  'Authorization': authorization,
}

res = requests.get(server_url + '/v1/accounts',headers=headers)
print(res.json())