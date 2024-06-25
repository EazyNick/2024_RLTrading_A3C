import time
import sys
import logging
from pathlib import Path
from celery import shared_task
from modules.utils import *
from modules.config.config import Config

# 추가 경로 설정
sys.path.append(str(Path(__file__).resolve().parents[2] / 'modules'))

logger = logging.getLogger('celery')

try:
    from modules.Auth import *  # Auth 모듈의 파일들을 임포트
    from modules.services import *  # services 모듈의 파일들을 임포트
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
            log_manager.logger.info("Access Token Update")
        else:
            log_manager.logger.error("Failed to load access token from file")
            access_token = manager.get_access_token()
    return access_token

@shared_task
def run_task():
    log_manager.logger.info("Start MainRun")
    print("Running...")
    key = KeyringManager()
    app_key = key.app_key
    app_secret = key.app_secret_key

    manager = AccessTokenManager()
    access_token = get_access_token(manager)

    stck_prpr = get_price(access_token, app_key, app_secret)
    # if stck_prpr:
        # log_manager.logger.info(f"현재가: {stck_prpr}")
        # DynamoDB에 데이터 저장 (IAM 권한으로 접근)
        # table.put_item(
        #     Item={
        #         'timestamp': int(time.time()),
        #         'stock_price': stck_prpr
        #     }
        # )

    return stck_prpr
