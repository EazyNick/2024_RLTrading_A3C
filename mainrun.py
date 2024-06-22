import time
import sys
import os
from pathlib import Path
from utils import *
from config.config import Config

try:
    # 현재 파일의 부모 디렉토리의 부모 디렉토리까지 경로 추가 및 auth_dir 추가
    sys.path.append(str(Path(__file__).resolve().parents[0] / 'Auth'))
    sys.path.append(str(Path(__file__).resolve().parents[0] / 'services'))

    from Auth import *
    from services import *
except ImportError as e:
    print(f"Import error: {e}")
    raise


import logging

# BASE_DIR와 LOG_DIR를 명확히 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'utils/Log')

# 로그 디렉토리가 존재하지 않으면 생성
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, 'mainrun.log')

# 로그 설정
logging.basicConfig(level=logging.INFO,
                    filename=LOG_FILE,
                    filemode='a',
                    format='[%(asctime)s] [%(levelname)s] %(message)s')

logger = logging.getLogger(__name__)

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
    log_manager.logger.info("Start MainRun")
    logging.info("Run function is starting...")
    print("Running...")
    key = KeyringManager()
    app_key = key.app_key
    app_secret = key.app_secret_key

    manager = AccessTokenManager()
    access_token = get_access_token(manager)

    stck_prpr = get_price(access_token, app_key, app_secret)
    if stck_prpr:
        log_manager.logger(f"현재가: {stck_prpr}")
    logging.info("Run function has finished.")

if __name__ == "__main__":
    for i in range(10):
        Run()
        time.sleep(1)
