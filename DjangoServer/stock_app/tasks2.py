import sys
import time
from pathlib import Path
from celery import shared_task
import boto3
from modules.utils import *
from modules.config.config import Config
import sys
import os
from decimal import Decimal


# 현재 파일의 디렉토리 경로
current_dir = os.path.dirname(os.path.abspath(__file__))

# dynamodb_to_csv.py 파일이 있는 디렉토리 경로
dynamodb_to_csv_dir = os.path.join(current_dir, '../RLmodels/data/DynamoDB')

# 모듈 경로에 추가
sys.path.append(dynamodb_to_csv_dir)

# 추가 경로 설정
sys.path.append(str(Path(__file__).resolve().parents[2] / 'modules'))

try:
    from modules.Auth import *  # Auth 모듈의 파일들을 임포트
    from modules.services import *  # services 모듈의 파일들을 임포트
    # dynamodb_to_csv 모듈 임포트
    from dynamodb_to_csv import convert_dynamodb_to_csv
except ImportError as e:
    print(f"Import error: {e}")
    raise

# DynamoDB 클라이언트 초기화
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
table = dynamodb.Table('StockPrices')

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

def calculate_sma(previous_sma, new_value, period=5):
    """
    단순 이동 평균(SMA)을 계산하는 함수
    Args:
        previous_sma (float): 이전 SMA 값
        new_value (float): 새로운 값
        period (int): 이동 평균 기간 (기본값은 5)
    Returns:
        float: 계산된 SMA 값
    """
    # 예제: 단순 이동 평균 계산 (더 복잡한 계산이 필요할 수 있음)
    return ((previous_sma * (period - 1)) + new_value) / period

def calculate_vma(previous_vma, new_volume, period=5):
    """
    거래량 이동 평균(VMA)을 계산하는 함수
    Args:
        previous_vma (float): 이전 VMA 값
        new_volume (int): 새로운 거래량 값
        period (int): 이동 평균 기간 (기본값은 5)
    Returns:
        float: 계산된 VMA 값
    """
    # 예제: 거래량 이동 평균 계산 (더 복잡한 계산이 필요할 수 있음)
    return ((previous_vma * (period - 1)) + new_volume) / period

def convert_to_decimal(data):
    """
    데이터를 Decimal 타입으로 변환하는 함수
    Args:
        data (dict): 변환할 데이터
    Returns:
        dict: Decimal 타입으로 변환된 데이터
    """
    for key, value in data.items():
        if isinstance(value, float):
            data[key] = Decimal(str(value))
        elif isinstance(value, dict):
            data[key] = convert_to_decimal(value)
    return data

@shared_task
def run_task2():
    log_manager.logger.info("Start MainRun2")
    print("Running...")

    # 키 관리자를 통해 키를 가져옵니다.
    key = KeyringManager()
    app_key = key.app_key   
    app_secret = key.app_secret_key

    # 액세스 토큰 관리자를 통해 토큰을 가져옵니다.
    manager = AccessTokenManager()
    access_token = get_access_token(manager)

    # 주식 데이터(현재가와 거래량)를 가져옵니다.
    stock_data = get_price(access_token, app_key, app_secret, div_code='J', itm_no='000270')

    if stock_data:
        log_manager.logger.info(f"현재가, 거래량: {stock_data}")

        # Decimal로 변환
        stock_data['Close'] = Decimal(str(stock_data['Close']))
        stock_data['Volume'] = Decimal(str(stock_data['Volume']))

        # DynamoDB에 연결합니다.
        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
        table = dynamodb.Table('StockPrices')

        # 기존 데이터를 읽어옵니다.
        existing_data = table.get_item(Key={'Date': stock_data['Date']})
        try:  
            sma_keys = [f'SMA_{i}' for i in range(5, 701, 10)]
            vma_keys = [f'VMA_{i}' for i in range(5, 701, 10)]

            if 'Item' in existing_data:
                log_manager.logger.info(f"기존 데이터가 존재합니다. 업데이트: {existing_data}")
                item = existing_data['Item']    

                new_item = {
                    'Date': stock_data['Date'],
                    'Close': Decimal(stock_data['Close']),
                    'Volume': Decimal(stock_data['Volume'])
                }

                for sma_key, vma_key in zip(sma_keys, vma_keys):
                    previous_sma = Decimal(item.get(sma_key, stock_data['Close']))
                    previous_vma = Decimal(item.get(vma_key, stock_data['Volume']))
                    new_item[sma_key] = calculate_sma(previous_sma, Decimal(stock_data['Close']))
                    new_item[vma_key] = calculate_vma(previous_vma, Decimal(stock_data['Volume']))

                new_item.update({
                    '365D_High': max(Decimal(item.get('365D_High', Decimal('0.0'))), stock_data['Close']),
                    '365D_Low': min(Decimal(item.get('365D_Low', Decimal('inf'))), stock_data['Close']),
                    '180D_High': max(Decimal(item.get('180D_High', Decimal('0.0'))), stock_data['Close']),
                    '180D_Low': min(Decimal(item.get('180D_Low', Decimal('inf'))), stock_data['Close']),
                    '90D_High': max(Decimal(item.get('90D_High', Decimal('0.0'))), stock_data['Close']),
                    '90D_Low': min(Decimal(item.get('90D_Low', Decimal('inf'))), stock_data['Close']),
                    '30D_High': max(Decimal(item.get('30D_High', Decimal('0.0'))), stock_data['Close']),
                    '30D_Low': min(Decimal(item.get('30D_Low', Decimal('inf'))), stock_data['Close']),
                    'AllTime_High': max(Decimal(item.get('AllTime_High', Decimal('0.0'))), stock_data['Close']),
                    'AllTime_Low': min(Decimal(item.get('AllTime_Low', Decimal('inf'))), stock_data['Close'])
                })

                response = table.put_item(Item=new_item)
                # log_manager.logger.debug(f"DynamoDB response: {response}")
                convert_dynamodb_to_csv()
            else:
                log_manager.logger.info("기존 데이터가 없습니다. 새 데이터로 추가합니다.")
                
                new_item = {
                    'Date': stock_data['Date'],
                    'Close': Decimal(stock_data['Close']),
                    'Volume': Decimal(stock_data['Volume']),
                    'SMA_5': Decimal(stock_data['Close']),  # 초기값 설정
                    'VMA_5': Decimal(stock_data['Volume']),
                }
                
                for sma_key, vma_key in zip(sma_keys[1:], vma_keys[1:]):
                    new_item[sma_key] = Decimal(stock_data['Close'])
                    new_item[vma_key] = Decimal(stock_data['Volume'])

                new_item.update({
                    '365D_High': Decimal(stock_data['Close']),
                    '365D_Low': Decimal(stock_data['Close']),
                    '180D_High': Decimal(stock_data['Close']),
                    '180D_Low': Decimal(stock_data['Close']),
                    '90D_High': Decimal(stock_data['Close']),
                    '90D_Low': Decimal(stock_data['Close']),
                    '30D_High': Decimal(stock_data['Close']),
                    '30D_Low': Decimal(stock_data['Close']),
                    'AllTime_High': Decimal(stock_data['Close']),
                    'AllTime_Low': Decimal(stock_data['Close'])
                })

                response = table.put_item(Item=new_item)
                # log_manager.logger.debug(f"DynamoDB response: {response}")
                convert_dynamodb_to_csv()
        except Exception as e:
            log_manager.logger.error(f"Error inserting data into DynamoDB: {e}")
    else:
        log_manager.logger.error("현재가 불러오기 실패")


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