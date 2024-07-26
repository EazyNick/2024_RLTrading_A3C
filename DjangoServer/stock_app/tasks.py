import sys
import time
from pathlib import Path
from celery import shared_task
import boto3
from modules.utils import *
from modules.config.config import Config

# 추가 경로 설정
sys.path.append(str(Path(__file__).resolve().parents[2] / 'modules'))

try:
    from modules.Auth import *  # Auth 모듈의 파일들을 임포트
    from modules.services import *  # services 모듈의 파일들을 임포트
except ImportError as e:
    print(f"Import error: {e}")
    raise

# DynamoDB 클라이언트 초기화
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
table = dynamodb.Table('RESTAPI')

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

    stock_data = get_price(access_token, app_key, app_secret)

    # if stock_data:
    #     log_manager.logger.info(f"현재가, 거래량: {stock_data}")
    # else:
    #     log_manager.logger.error(f"현재가 불러오기 실패")

    # if stck_prpr:
    #     log_manager.logger.info(f"Insert 현재가: {stck_prpr}")
    # # DynamoDB에 데이터 저장
    #     try:
    #         response = table.put_item(
    #             Item={
    #                 'Stock': '삼성전자',  # 예시 Stock
    #                 'Timestamp': str(int(time.time())), 
    #                 '현재가': str(stck_prpr)  # 주식 현재가
    #             }
    #         )
    #         log_manager.logger.info(f"Data saved to DynamoDB successfully: {response}")
    #     except Exception as e:
    #         log_manager.logger.error(f"Failed to save data to DynamoDB: {e}")
    #         raise
    # else:
    #     log_manager.logger.warning("stck_prpr is None or False-like value")

    # # 디버깅 로그 추가
    # log_manager.logger.debug("Before buy_stock")

    # try:
    #     buy_data = buy_stock(access_token, app_key, app_secret, "70000")
    #     if buy_data:
    #         log_manager.logger.info(f"주식 매수: {buy_data}")
    #     else:
    #         log_manager.logger.error(f"매수 실패")
    # except Exception as e:
    #     log_manager.logger.error(f"buy_stock 예외 발생: {e}")

    # log_manager.logger.debug("Before sell_stock")
    # try:
    #     sell_data = sell_stock(access_token, app_key, app_secret, "90000")
    #     if sell_data:
    #         log_manager.logger.info(f"주식 매도: {sell_data}")
    #     else:
    #         log_manager.logger.error(f"매도 실패")
    # except Exception as e:
    #     log_manager.logger.error(f"sell_stock 예외 발생: {e}")


    # log_manager.logger.debug("Before get_account_balance")
    # try:
    #     account = get_account_balance(access_token, app_key, app_secret)
    #     if account:
    #         log_manager.logger.info(f"계좌 현황: {account}")
    #     else:
    #         log_manager.logger.error(f"계좌 조회 실패")
    # except Exception as e:
    #     log_manager.logger.error(f"get_account_balance 예외 발생: {e}")
    
    # return stck_prpr