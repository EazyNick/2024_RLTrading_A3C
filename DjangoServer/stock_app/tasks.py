import sys
from pathlib import Path
from celery import shared_task
import boto3
from modules.utils import *
from modules.config.config import Config
from stock_app.tasks2 import run_task2
import datetime
from datetime import datetime
from datetime import datetime
import pytz  # 한국 시간을 사용하기 위해 필요

# 추가 경로 설정
sys.path.append(str(Path(__file__).resolve().parent / 'modules'))
sys.path.append(str(Path(__file__).resolve().parent / 'RLmodels'))
sys.path.append(str(Path(__file__).resolve().parent / 'ChatGPT'))

try:
    from modules.Auth import *  # Auth 모듈의 파일들을 임포트
    from modules.services import *  # services 모듈의 파일들을 임포트
    from RLmodels.main import main_run
    from RLmodels.Agent.A3CAgent import A3CAgent  # A3CAgent 클래스 불러오기
    from RLmodels.env.env import StockTradingEnv
    from modules.utils import *
    from modules.config import *
    from ChatGPT.API import *
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
        # access_token = manager.get_access_token()  # get_access_token 메서드 호출하여 access_token 가져오기
        Config.Base.increment_flag()
    else:
        access_token = manager.load_access_token()
        if access_token:
            log_manager.logger.info("Access Token Update")
        else:
            log_manager.logger.error("Failed to load access token from file")
            access_token = manager.get_access_token()
    return access_token

# 1달 기준
def filter_logs_by_current_month(buy_sell_log):
    current_year = datetime.now().year
    current_month = datetime.now().month

    filtered_log = [
        log for log in buy_sell_log
        if log[0].year == current_year and log[0].month == current_month
    ]
    return filtered_log

# 1주 기준
def filter_logs_by_current_week(buy_sell_log):
    current_year, current_week, _ = datetime.now().isocalendar()

    filtered_log = [
        log for log in buy_sell_log
        if log[0].isocalendar()[0] == current_year and log[0].isocalendar()[1] == current_week
    ]
    return filtered_log

@shared_task
def run_task():
    log_manager.logger.info("자동매매 시작")
    log_manager.logger.info("Running...")
    
    # # Task 2 실행
    # result = run_task2.delay()
    # task_result = result.get()
    # log_manager.logger.info("Task 2 결과:", task_result)

    # 한국 시간대 설정
    tz = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(tz).time()

    # 오전 9시부터 오후 3시 20분 사이에만 실행
    start_time = datetime.strptime("09:00", "%H:%M").time()
    end_time = datetime.strptime("15:30", "%H:%M").time()

    if start_time <= current_time <= end_time:

        key = KeyringManager()
        app_key = key.app_key
        app_secret = key.app_secret_key

        manager = AccessTokenManager()
        access_token = get_access_token(manager)

        try:
            stock_info_list, account_info = get_account_balance(access_token, app_key, app_secret)
        
            if stock_info_list is not None and account_info is not None:
                formatter = AccountFormatter()
                formatter.format(stock_info_list, account_info)
                dynamodbmanager = DynamoDBManager()
                dynamodbmanager.save_to_dynamodb('admin', stock_info_list, account_info)
            else:
                log_manager.logger.error("Failed to retrieve account information")
        except Exception as e:
            log_manager.logger.error(f"get_account_balance 예외 발생: {e}")

        try:
            log_manager.logger.info(f"모델 실행 시작")
            buy_sell_log = main_run()
            log_manager.logger.debug(f"Buy dates: {buy_sell_log}")
            log_manager.logger.info(f"모델 실행 완료")

            # 이번 달에 매수, 매도한 기록만 필터링
            filtered_buy_sell_log = filter_logs_by_current_week(buy_sell_log)
            log_manager.logger.info(f"filtered_buy_sell_log: {filtered_buy_sell_log}")

            # -1000 ~ 1000사이의 점수 반환, GPT 스코어 반환함수로, 비용문제로 주석처리 해둠
            score = API_main()
            # score = 50

            # chat gpt의 매매 점수가 900이상(과매수)
            if score < 900:
                # 매수, 매도 시점의 로그
                for log in filtered_buy_sell_log:
                    date, action, num_stocks, price = log
                    price = str(int(price))  # np.float64 값을 일반 정수로 변환
                    log_manager.logger.debug(f"Processing {action} action for {num_stocks} stocks at {price} on {date}")
                    if action == 'buy':
                        buy_data = buy_stock(access_token, app_key, app_secret, price)
                        if buy_data:
                            log_manager.logger.info(f"주식 매수: {buy_data}")
                        else:
                            log_manager.logger.error(f"매수 실패")
                        log_manager.logger.info(f"Buy signal on {date} for {num_stocks} stocks at {price}")
                    elif action == 'sell':
                        sell_data = sell_stock(access_token, app_key, app_secret, price)
                        if sell_data:
                            log_manager.logger.info(f"주식 매도: {sell_data}")
                        else:
                            log_manager.logger.error(f"매도 실패")
                        log_manager.logger.info(f"Sell signal on {date} for {num_stocks} stocks at {price}")
            else:
                log_manager.logger.info(f"과매수 구간입니다. Chat GPT 추천점수는 {score}점 입니다.")
                pass
        except ImportError as e:
            log_manager.logger.error(f"모델 실행 실패: {e}")
        except Exception as e:
            log_manager.logger.error(f"예상치 못한 에러 발생: {e}")
    else:
        log_manager.logger.info(f"현재 시간({current_time})은 작업 시간대가 아닙니다. 주식 자동매매는 9시부터 15시 30분 사이에만 실행됩니다.")