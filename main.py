import json
import requests
import pandas as pd
import sys, os
from utils import *

# Secret 디렉토리를 sys.path에 추가하여 모듈을 찾을 수 있도록 설정
try:
  current_dir = os.path.dirname(os.path.abspath(__file__))
  secret_dir = os.path.join(current_dir, 'Auth')
  sys.path.append(secret_dir)
  from Auth import *
except:
  from Auth import *

def Run():
    key = KeyringManager()
    app_key = key.app_key
    app_secret = key.app_secret_key

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
    at_temp = res.json()['access_token']

    if at_temp:
        save_access_token(at_temp)
        access_token = load_access_token()
        log_manager.logger.info("Loaded Access Token")
    else:
        log_manager.logger.error("Failed to retrieve access token")

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

if __name__ == "__main__":
   Run()