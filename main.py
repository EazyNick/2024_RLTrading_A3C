import time
import sys
import os
from utils import *
from config.config import Config

# Auth 모듈 및 services 모듈 임포트
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    secret_dir = os.path.join(current_dir, 'Auth')
    services_dir = os.path.join(current_dir, 'services')
    sys.path.append(secret_dir)
    sys.path.append(services_dir)
    from Auth import *
    from services import *
except ImportError as e:
    print(f"Import error: {e}")
    raise

def get_access_token(manager):
    """
    액세스 토큰을 가져오는 함수

    Args:
        manager (AccessTokenManager): 액세스 토큰을 관리하는 AccessTokenManager 인스턴스

    Returns:
        str: 성공적으로 가져온 액세스 토큰
    """
    if Config.Base.get_flag() == 0:
        access_token = manager.get_access_token()  # get_access_token 메서드 호출하여 access_token 가져오기
        Config.Base.increment_flag()
    else:
        access_token = manager.load_access_token()
        if access_token:
            log_manager.logger.info("Loaded Access Token")
        else:
            log_manager.logger.error("Failed to load access token from file")
            access_token = manager.get_access_token()
    return access_token

def Run():
    key = KeyringManager()
    app_key = key.app_key
    app_secret = key.app_secret_key

    manager = AccessTokenManager()
    access_token = get_access_token(manager)

    stck_prpr = get_price(access_token, app_key, app_secret)
    if stck_prpr:
        print(f"현재가: {stck_prpr}")

if __name__ == "__main__":
    for i in range(10):
        Run()
        time.sleep(1)
