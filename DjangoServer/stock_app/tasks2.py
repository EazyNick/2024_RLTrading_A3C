import sys
import time
from pathlib import Path
from celery import shared_task
import boto3
from modules.utils import *
from modules.config.config import Config
import sys
import os


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
    import dynamodb_to_csv
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

@shared_task
def run_task():
    log_manager.logger.info("Start MainRun")
    print("Running...")

    # 키 관리자를 통해 키를 가져옵니다.
    key = KeyringManager()
    app_key = key.app_key
    app_secret = key.app_secret_key

    # 액세스 토큰 관리자를 통해 토큰을 가져옵니다.
    manager = AccessTokenManager()
    access_token = get_access_token(manager)

    # 주식 데이터(현재가와 거래량)를 가져옵니다.
    stock_data = get_price(access_token, app_key, app_secret)

    if stock_data:
        log_manager.logger.info(f"현재가, 거래량: {stock_data}")

        # DynamoDB에 연결합니다.
        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
        table = dynamodb.Table('StockPrices')

        # 기존 데이터를 읽어옵니다.
        existing_data = table.get_item(Key={'Date': stock_data['Date']})
        if 'Item' in existing_data:
            item = existing_data['Item']
            # log_manager.logger.debug(f"기존 데이터: {item}")

            # 필요한 계산을 수행합니다.
            # 예시로, 이전 SMA 값을 가져와서 새로운 SMA 값을 계산합니다.
            # 여기서는 간단히 기존 값을 사용하고 있지만, 실제로는 원하는 계산을 수행해야 합니다.

            new_item = {
                'Date': stock_data['Date'],
                'Close': stock_data['Close'],
                'Volume': stock_data['Volume'],
                'SMA_5': calculate_sma(item.get('SMA_5'), stock_data['Close']),
                'VMA_5': calculate_vma(item.get('VMA_5'), stock_data['Volume']),
                'SMA_10': calculate_sma(item.get('SMA_10'), stock_data['Close']),
                'VMA_10': calculate_vma(item.get('VMA_10'), stock_data['Volume']),
                'SMA_15': calculate_sma(item.get('SMA_15'), stock_data['Close']),
                'VMA_15': calculate_vma(item.get('VMA_15'), stock_data['Volume']),
                'SMA_20': calculate_sma(item.get('SMA_20'), stock_data['Close']),
                'VMA_20': calculate_vma(item.get('VMA_20'), stock_data['Volume']),
                'SMA_25': calculate_sma(item.get('SMA_25'), stock_data['Close']),
                'VMA_25': calculate_vma(item.get('VMA_25'), stock_data['Volume']),
                'SMA_30': calculate_sma(item.get('SMA_30'), stock_data['Close']),
                'VMA_30': calculate_vma(item.get('VMA_30'), stock_data['Volume']),
                'SMA_35': calculate_sma(item.get('SMA_35'), stock_data['Close']),
                'VMA_35': calculate_vma(item.get('VMA_35'), stock_data['Volume']),
                'SMA_40': calculate_sma(item.get('SMA_40'), stock_data['Close']),
                'VMA_40': calculate_vma(item.get('VMA_40'), stock_data['Volume']),
                'SMA_45': calculate_sma(item.get('SMA_45'), stock_data['Close']),
                'VMA_45': calculate_vma(item.get('VMA_45'), stock_data['Volume']),
                'SMA_50': calculate_sma(item.get('SMA_50'), stock_data['Close']),
                'VMA_50': calculate_vma(item.get('VMA_50'), stock_data['Volume']),
                'SMA_60': calculate_sma(item.get('SMA_60'), stock_data['Close']),
                'VMA_60': calculate_vma(item.get('VMA_60'), stock_data['Volume']),
                'SMA_70': calculate_sma(item.get('SMA_70'), stock_data['Close']),
                'VMA_70': calculate_vma(item.get('VMA_70'), stock_data['Volume']),
                'SMA_80': calculate_sma(item.get('SMA_80'), stock_data['Close']),
                'VMA_80': calculate_vma(item.get('VMA_80'), stock_data['Volume']),
                'SMA_90': calculate_sma(item.get('SMA_90'), stock_data['Close']),
                'VMA_90': calculate_vma(item.get('VMA_90'), stock_data['Volume']),
                'SMA_100': calculate_sma(item.get('SMA_100'), stock_data['Close']),
                'VMA_100': calculate_vma(item.get('VMA_100'), stock_data['Volume']),
                'SMA_110': calculate_sma(item.get('SMA_110'), stock_data['Close']),
                'VMA_110': calculate_vma(item.get('VMA_110'), stock_data['Volume']),
                'SMA_120': calculate_sma(item.get('SMA_120'), stock_data['Close']),
                'VMA_120': calculate_vma(item.get('VMA_120'), stock_data['Volume']),
                'SMA_130': calculate_sma(item.get('SMA_130'), stock_data['Close']),
                'VMA_130': calculate_vma(item.get('VMA_130'), stock_data['Volume']),
                'SMA_140': calculate_sma(item.get('SMA_140'), stock_data['Close']),
                'VMA_140': calculate_vma(item.get('VMA_140'), stock_data['Volume']),
                'SMA_150': calculate_sma(item.get('SMA_150'), stock_data['Close']),
                'VMA_150': calculate_vma(item.get('VMA_150'), stock_data['Volume']),
                'SMA_160': calculate_sma(item.get('SMA_160'), stock_data['Close']),
                'VMA_160': calculate_vma(item.get('VMA_160'), stock_data['Volume']),
                'SMA_170': calculate_sma(item.get('SMA_170'), stock_data['Close']),
                'VMA_170': calculate_vma(item.get('VMA_170'), stock_data['Volume']),
                'SMA_180': calculate_sma(item.get('SMA_180'), stock_data['Close']),
                'VMA_180': calculate_vma(item.get('VMA_180'), stock_data['Volume']),
                'SMA_190': calculate_sma(item.get('SMA_190'), stock_data['Close']),
                'VMA_190': calculate_vma(item.get('VMA_190'), stock_data['Volume']),
                'SMA_200': calculate_sma(item.get('SMA_200'), stock_data['Close']),
                'VMA_200': calculate_vma(item.get('VMA_200'), stock_data['Volume']),
                'SMA_210': calculate_sma(item.get('SMA_210'), stock_data['Close']),
                'VMA_210': calculate_vma(item.get('VMA_210'), stock_data['Volume']),
                'SMA_220': calculate_sma(item.get('SMA_220'), stock_data['Close']),
                'VMA_220': calculate_vma(item.get('VMA_220'), stock_data['Volume']),
                'SMA_230': calculate_sma(item.get('SMA_230'), stock_data['Close']),
                'VMA_230': calculate_vma(item.get('VMA_230'), stock_data['Volume']),
                'SMA_240': calculate_sma(item.get('SMA_240'), stock_data['Close']),
                'VMA_240': calculate_vma(item.get('VMA_240'), stock_data['Volume']),
                'SMA_250': calculate_sma(item.get('SMA_250'), stock_data['Close']),
                'VMA_250': calculate_vma(item.get('VMA_250'), stock_data['Volume']),
                'SMA_260': calculate_sma(item.get('SMA_260'), stock_data['Close']),
                'VMA_260': calculate_vma(item.get('VMA_260'), stock_data['Volume']),
                'SMA_270': calculate_sma(item.get('SMA_270'), stock_data['Close']),
                'VMA_270': calculate_vma(item.get('VMA_270'), stock_data['Volume']),
                'SMA_280': calculate_sma(item.get('SMA_280'), stock_data['Close']),
                'VMA_280': calculate_vma(item.get('VMA_280'), stock_data['Volume']),
                'SMA_290': calculate_sma(item.get('SMA_290'), stock_data['Close']),
                'VMA_290': calculate_vma(item.get('VMA_290'), stock_data['Volume']),
                'SMA_300': calculate_sma(item.get('SMA_300'), stock_data['Close']),
                'VMA_300': calculate_vma(item.get('VMA_300'), stock_data['Volume']),
                'SMA_310': calculate_sma(item.get('SMA_310'), stock_data['Close']),
                'VMA_310': calculate_vma(item.get('VMA_310'), stock_data['Volume']),
                'SMA_320': calculate_sma(item.get('SMA_320'), stock_data['Close']),
                'VMA_320': calculate_vma(item.get('VMA_320'), stock_data['Volume']),
                'SMA_330': calculate_sma(item.get('SMA_330'), stock_data['Close']),
                'VMA_330': calculate_vma(item.get('VMA_330'), stock_data['Volume']),
                'SMA_340': calculate_sma(item.get('SMA_340'), stock_data['Close']),
                'VMA_340': calculate_vma(item.get('VMA_340'), stock_data['Volume']),
                'SMA_350': calculate_sma(item.get('SMA_350'), stock_data['Close']),
                'VMA_350': calculate_vma(item.get('VMA_350'), stock_data['Volume']),
                'SMA_360': calculate_sma(item.get('SMA_360'), stock_data['Close']),
                'VMA_360': calculate_vma(item.get('VMA_360'), stock_data['Volume']),
                'SMA_370': calculate_sma(item.get('SMA_370'), stock_data['Close']),
                'VMA_370': calculate_vma(item.get('VMA_370'), stock_data['Volume']),
                'SMA_380': calculate_sma(item.get('SMA_380'), stock_data['Close']),
                'VMA_380': calculate_vma(item.get('VMA_380'), stock_data['Volume']),
                'SMA_390': calculate_sma(item.get('SMA_390'), stock_data['Close']),
                'VMA_390': calculate_vma(item.get('VMA_390'), stock_data['Volume']),
                'SMA_400': calculate_sma(item.get('SMA_400'), stock_data['Close']),
                'VMA_400': calculate_vma(item.get('VMA_400'), stock_data['Volume']),
                'SMA_410': calculate_sma(item.get('SMA_410'), stock_data['Close']),
                'VMA_410': calculate_vma(item.get('VMA_410'), stock_data['Volume']),
                'SMA_420': calculate_sma(item.get('SMA_420'), stock_data['Close']),
                'VMA_420': calculate_vma(item.get('VMA_420'), stock_data['Volume']),
                'SMA_430': calculate_sma(item.get('SMA_430'), stock_data['Close']),
                'VMA_430': calculate_vma(item.get('VMA_430'), stock_data['Volume']),
                'SMA_440': calculate_sma(item.get('SMA_440'), stock_data['Close']),
                'VMA_440': calculate_vma(item.get('VMA_440'), stock_data['Volume']),
                'SMA_450': calculate_sma(item.get('SMA_450'), stock_data['Close']),
                'VMA_450': calculate_vma(item.get('VMA_450'), stock_data['Volume']),
                'SMA_460': calculate_sma(item.get('SMA_460'), stock_data['Close']),
                'VMA_460': calculate_vma(item.get('VMA_460'), stock_data['Volume']),
                'SMA_470': calculate_sma(item.get('SMA_470'), stock_data['Close']),
                'VMA_470': calculate_vma(item.get('VMA_470'), stock_data['Volume']),
                'SMA_480': calculate_sma(item.get('SMA_480'), stock_data['Close']),
                'VMA_480': calculate_vma(item.get('VMA_480'), stock_data['Volume']),
                'SMA_490': calculate_sma(item.get('SMA_490'), stock_data['Close']),
                'VMA_490': calculate_vma(item.get('VMA_490'), stock_data['Volume']),
                'SMA_500': calculate_sma(item.get('SMA_500'), stock_data['Close']),
                'VMA_500': calculate_vma(item.get('VMA_500'), stock_data['Volume']),
                'SMA_510': calculate_sma(item.get('SMA_510'), stock_data['Close']),
                'VMA_510': calculate_vma(item.get('VMA_510'), stock_data['Volume']),
                'SMA_520': calculate_sma(item.get('SMA_520'), stock_data['Close']),
                'VMA_520': calculate_vma(item.get('VMA_520'), stock_data['Volume']),
                'SMA_530': calculate_sma(item.get('SMA_530'), stock_data['Close']),
                'VMA_530': calculate_vma(item.get('VMA_530'), stock_data['Volume']),
                'SMA_540': calculate_sma(item.get('SMA_540'), stock_data['Close']),
                'VMA_540': calculate_vma(item.get('VMA_540'), stock_data['Volume']),
                'SMA_550': calculate_sma(item.get('SMA_550'), stock_data['Close']),
                'VMA_550': calculate_vma(item.get('VMA_550'), stock_data['Volume']),
                'SMA_560': calculate_sma(item.get('SMA_560'), stock_data['Close']),
                'VMA_560': calculate_vma(item.get('VMA_560'), stock_data['Volume']),
                'SMA_570': calculate_sma(item.get('SMA_570'), stock_data['Close']),
                'VMA_570': calculate_vma(item.get('VMA_570'), stock_data['Volume']),
                'SMA_580': calculate_sma(item.get('SMA_580'), stock_data['Close']),
                'VMA_580': calculate_vma(item.get('VMA_580'), stock_data['Volume']),
                'SMA_590': calculate_sma(item.get('SMA_590'), stock_data['Close']),
                'VMA_590': calculate_vma(item.get('VMA_590'), stock_data['Volume']),
                'SMA_600': calculate_sma(item.get('SMA_600'), stock_data['Close']),
                'VMA_600': calculate_vma(item.get('VMA_600'), stock_data['Volume']),
                'SMA_610': calculate_sma(item.get('SMA_610'), stock_data['Close']),
                'VMA_610': calculate_vma(item.get('VMA_610'), stock_data['Volume']),
                'SMA_620': calculate_sma(item.get('SMA_620'), stock_data['Close']),
                'VMA_620': calculate_vma(item.get('VMA_620'), stock_data['Volume']),
                'SMA_630': calculate_sma(item.get('SMA_630'), stock_data['Close']),
                'VMA_630': calculate_vma(item.get('VMA_630'), stock_data['Volume']),
                'SMA_640': calculate_sma(item.get('SMA_640'), stock_data['Close']),
                'VMA_640': calculate_vma(item.get('VMA_640'), stock_data['Volume']),
                'SMA_650': calculate_sma(item.get('SMA_650'), stock_data['Close']),
                'VMA_650': calculate_vma(item.get('VMA_650'), stock_data['Volume']),
                'SMA_660': calculate_sma(item.get('SMA_660'), stock_data['Close']),
                'VMA_660': calculate_vma(item.get('VMA_660'), stock_data['Volume']),
                'SMA_670': calculate_sma(item.get('SMA_670'), stock_data['Close']),
                'VMA_670': calculate_vma(item.get('VMA_670'), stock_data['Volume']),
                'SMA_680': calculate_sma(item.get('SMA_680'), stock_data['Close']),
                'VMA_680': calculate_vma(item.get('VMA_680'), stock_data['Volume']),
                'SMA_690': calculate_sma(item.get('SMA_690'), stock_data['Close']),
                'VMA_690': calculate_vma(item.get('VMA_690'), stock_data['Volume']),
                'SMA_700': calculate_sma(item.get('SMA_700'), stock_data['Close']),
                'VMA_700': calculate_vma(item.get('VMA_700'), stock_data['Volume']),
                '365D_High': max(item.get('365D_High', 0.0), stock_data['Close']),
                '365D_Low': min(item.get('365D_Low', float('inf')), stock_data['Close']),
                '180D_High': max(item.get('180D_High', 0.0), stock_data['Close']),
                '180D_Low': min(item.get('180D_Low', float('inf')), stock_data['Close']),
                '90D_High': max(item.get('90D_High', 0.0), stock_data['Close']),
                '90D_Low': min(item.get('90D_Low', float('inf')), stock_data['Close']),
                '30D_High': max(item.get('30D_High', 0.0), stock_data['Close']),
                '30D_Low': min(item.get('30D_Low', float('inf')), stock_data['Close']),
                'AllTime_High': max(item.get('AllTime_High', 0.0), stock_data['Close']),
                'AllTime_Low': min(item.get('AllTime_Low', float('inf')), stock_data['Close'])
            }

            # DynamoDB에 데이터를 업데이트합니다.
            table.put_item(Item=new_item)
            # dynamodb_to_csv.py 파일의 함수 사용 예시
            dynamodb_to_csv.convert_dynamodb_to_csv()  # 파일 내 함수 이름에 맞게 수정
        else:
            log_manager.logger.info("기존 데이터가 없습니다. 새 데이터로 추가합니다.")
            # 초기 값을 설정하여 새로운 데이터로 추가합니다.
            new_item = {
                'Date': stock_data['Date'],
                'Close': stock_data['Close'],
                'Volume': stock_data['Volume'],
                'SMA_5': stock_data['Close'],  # 초기값 설정
                'VMA_5': stock_data['Volume'],
                'SMA_10': stock_data['Close'],
                'VMA_10': stock_data['Volume'],
                'SMA_15': stock_data['Close'],
                'VMA_15': stock_data['Volume'],
                'SMA_20': stock_data['Close'],
                'VMA_20': stock_data['Volume'],
                'SMA_25': stock_data['Close'],
                'VMA_25': stock_data['Volume'],
                'SMA_30': stock_data['Close'],
                'VMA_30': stock_data['Volume'],
                'SMA_35': stock_data['Close'],
                'VMA_35': stock_data['Volume'],
                'SMA_40': stock_data['Close'],
                'VMA_40': stock_data['Volume'],
                'SMA_45': stock_data['Close'],
                'VMA_45': stock_data['Volume'],
                'SMA_50': stock_data['Close'],
                'VMA_50': stock_data['Volume'],
                'SMA_60': stock_data['Close'],
                'VMA_60': stock_data['Volume'],
                'SMA_70': stock_data['Close'],
                'VMA_70': stock_data['Volume'],
                'SMA_80': stock_data['Close'],
                'VMA_80': stock_data['Volume'],
                'SMA_90': stock_data['Close'],
                'VMA_90': stock_data['Volume'],
                'SMA_100': stock_data['Close'],
                'VMA_100': stock_data['Volume'],
                'SMA_110': stock_data['Close'],
                'VMA_110': stock_data['Volume'],
                'SMA_120': stock_data['Close'],
                'VMA_120': stock_data['Volume'],
                'SMA_130': stock_data['Close'],
                'VMA_130': stock_data['Volume'],
                'SMA_140': stock_data['Close'],
                'VMA_140': stock_data['Volume'],
                'SMA_150': stock_data['Close'],
                'VMA_150': stock_data['Volume'],
                'SMA_160': stock_data['Close'],
                'VMA_160': stock_data['Volume'],
                'SMA_170': stock_data['Close'],
                'VMA_170': stock_data['Volume'],
                'SMA_180': stock_data['Close'],
                'VMA_180': stock_data['Volume'],
                'SMA_190': stock_data['Close'],
                'VMA_190': stock_data['Volume'],
                'SMA_200': stock_data['Close'],
                'VMA_200': stock_data['Volume'],
                'SMA_210': stock_data['Close'],
                'VMA_210': stock_data['Volume'],
                'SMA_220': stock_data['Close'],
                'VMA_220': stock_data['Volume'],
                'SMA_230': stock_data['Close'],
                'VMA_230': stock_data['Volume'],
                'SMA_240': stock_data['Close'],
                'VMA_240': stock_data['Volume'],
                'SMA_250': stock_data['Close'],
                'VMA_250': stock_data['Volume'],
                'SMA_260': stock_data['Close'],
                'VMA_260': stock_data['Volume'],
                'SMA_270': stock_data['Close'],
                'VMA_270': stock_data['Volume'],
                'SMA_280': stock_data['Close'],
                'VMA_280': stock_data['Volume'],
                'SMA_290': stock_data['Close'],
                'VMA_290': stock_data['Volume'],
                'SMA_300': stock_data['Close'],
                'VMA_300': stock_data['Volume'],
                'SMA_310': stock_data['Close'],
                'VMA_310': stock_data['Volume'],
                'SMA_320': stock_data['Close'],
                'VMA_320': stock_data['Volume'],
                'SMA_330': stock_data['Close'],
                'VMA_330': stock_data['Volume'],
                'SMA_340': stock_data['Close'],
                'VMA_340': stock_data['Volume'],
                'SMA_350': stock_data['Close'],
                'VMA_350': stock_data['Volume'],
                'SMA_360': stock_data['Close'],
                'VMA_360': stock_data['Volume'],
                'SMA_370': stock_data['Close'],
                'VMA_370': stock_data['Volume'],
                'SMA_380': stock_data['Close'],
                'VMA_380': stock_data['Volume'],
                'SMA_390': stock_data['Close'],
                'VMA_390': stock_data['Volume'],
                'SMA_400': stock_data['Close'],
                'VMA_400': stock_data['Volume'],
                'SMA_410': stock_data['Close'],
                'VMA_410': stock_data['Volume'],
                'SMA_420': stock_data['Close'],
                'VMA_420': stock_data['Volume'],
                'SMA_430': stock_data['Close'],
                'VMA_430': stock_data['Volume'],
                'SMA_440': stock_data['Close'],
                'VMA_440': stock_data['Volume'],
                'SMA_450': stock_data['Close'],
                'VMA_450': stock_data['Volume'],
                'SMA_460': stock_data['Close'],
                'VMA_460': stock_data['Volume'],
                'SMA_470': stock_data['Close'],
                'VMA_470': stock_data['Volume'],
                'SMA_480': stock_data['Close'],
                'VMA_480': stock_data['Volume'],
                'SMA_490': stock_data['Close'],
                'VMA_490': stock_data['Volume'],
                'SMA_500': stock_data['Close'],
                'VMA_500': stock_data['Volume'],
                'SMA_510': stock_data['Close'],
                'VMA_510': stock_data['Volume'],
                'SMA_520': stock_data['Close'],
                'VMA_520': stock_data['Volume'],
                'SMA_530': stock_data['Close'],
                'VMA_530': stock_data['Volume'],
                'SMA_540': stock_data['Close'],
                'VMA_540': stock_data['Volume'],
                'SMA_550': stock_data['Close'],
                'VMA_550': stock_data['Volume'],
                'SMA_560': stock_data['Close'],
                'VMA_560': stock_data['Volume'],
                'SMA_570': stock_data['Close'],
                'VMA_570': stock_data['Volume'],
                'SMA_580': stock_data['Close'],
                'VMA_580': stock_data['Volume'],
                'SMA_590': stock_data['Close'],
                'VMA_590': stock_data['Volume'],
                'SMA_600': stock_data['Close'],
                'VMA_600': stock_data['Volume'],
                'SMA_610': stock_data['Close'],
                'VMA_610': stock_data['Volume'],
                'SMA_620': stock_data['Close'],
                'VMA_620': stock_data['Volume'],
                'SMA_630': stock_data['Close'],
                'VMA_630': stock_data['Volume'],
                'SMA_640': stock_data['Close'],
                'VMA_640': stock_data['Volume'],
                'SMA_650': stock_data['Close'],
                'VMA_650': stock_data['Volume'],
                'SMA_660': stock_data['Close'],
                'VMA_660': stock_data['Volume'],
                'SMA_670': stock_data['Close'],
                'VMA_670': stock_data['Volume'],
                'SMA_680': stock_data['Close'],
                'VMA_680': stock_data['Volume'],
                'SMA_690': stock_data['Close'],
                'VMA_690': stock_data['Volume'],
                'SMA_700': stock_data['Close'],
                'VMA_700': stock_data['Volume'],
                '365D_High': stock_data['Close'],
                '365D_Low': stock_data['Close'],
                '180D_High': stock_data['Close'],
                '180D_Low': stock_data['Close'],
                '90D_High': stock_data['Close'],
                '90D_Low': stock_data['Close'],
                '30D_High': stock_data['Close'],
                '30D_Low': stock_data['Close'],
                'AllTime_High': stock_data['Close'],
                'AllTime_Low': stock_data['Close']
            }
            table.put_item(Item=new_item)
            # dynamodb_to_csv.py 파일의 함수 사용 예시
            dynamodb_to_csv.convert_dynamodb_to_csv()  # 파일 내 함수 이름에 맞게 수정
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