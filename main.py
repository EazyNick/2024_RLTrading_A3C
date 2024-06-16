import keyring
import json
import requests
import pandas as pd

def hashkey(datas):
  PATH = "uapi/hashkey"
  URL = f"{url_base}/{path}"
  headers = {
    'content-Type' : 'application/json',
    'appKey' : app_key,
    'appSecret' : app_secret,
    }
  res = requests.post(URL, headers=headers, data=json.dumps(datas))
  hashkey = res.json()["HASH"]

  return hashkey

app_key = keyring.get_password('mock_app_key', 'Henry')
app_secret = keyring.get_password('mock_app_secret', 'Henry')

# 모의투자 url
url_base = "https://openapivts.koreainvestment.com:29443"

headers = {"content-type": "application/json"}
path = "oauth2/tokenP"
body = {
    "grant_type": "client_credentials",
    "appkey": app_key,
    "appsecret": app_secret
}

url = f"{url_base}/{path}"
res = requests.post(url, headers=headers, data=json.dumps(body))
access_token = res.json()['access_token']

keyring.set_password('mock_access_token', 'Henry', access_token)

access_token = keyring.get_password('mock_access_token', 'Henry')

print(access_token)

# API 호출을 위한 URL 및 헤더 설정
url = "https://openapivts.koreainvestment.com:29443/uapi/domestic-stock/v1/quotations/inquire-price"
headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": f"Bearer {access_token}",
    "appkey": app_key,
    "appsecret": app_secret,
    "tr_id": "FHKST01010100"
}

div_code="J"
itm_no="005930" # 삼성전자

params = {
        "FID_COND_MRKT_DIV_CODE": div_code, # 시장 분류 코드  J : 주식/ETF/ETN, W: ELW
        "FID_INPUT_ISCD": itm_no            #   종목번호 (6자리) ETN의 경우, Q로 시작 (EX. Q500001)
    }

res = requests.get(url, headers=headers, params=params)
# current_data = pd.DataFrame(res.getBody().output, index=[0])
print(res.json())
# res.json()['output']['stck_prpr']