import sys
import time
from pathlib import Path
from celery import shared_task
import boto3
from modules.utils import *
from modules.config.config import Config
import os
from decimal import Decimal
import pandas as pd
from datetime import datetime
import pytz  # 한국 시간을 사용하기 위해 필요

try:
    # 현재 파일의 디렉토리 경로
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # dynamodb_to_csv.py 파일이 있는 디렉토리 경로
    dynamodb_to_csv_dir = os.path.join(current_dir, '../RLmodels/data/DynamoDB')
    # 모듈 경로에 추가
    sys.path.append(dynamodb_to_csv_dir)
    # 추가 경로 설정
    sys.path.append(str(Path(__file__).resolve().parents[2] / 'modules'))
    sys.path.append(str(Path(__file__).resolve().parents[2] / 'RLmodels'))

    from modules.Auth import *  # Auth 모듈의 파일들을 임포트
    from modules.services import *  # services 모듈의 파일들을 임포트
    from dynamodb_to_csv import convert_dynamodb_to_csv
except ImportError as e:
    print(f"Import error: {e}")
    raise

@shared_task
def run_task3():
    log_manager.logger.info("Task3 지수 데이터 저장 시작")  # 로그 추가
    print("Task3 Running...")

    # 코스피, 코스닥 5분봉 데이터 DynamoDB에 저장
    try:
        kospi_data_today = get_intraday_data('^KS11', interval='5m', period='1d')
        kosdaq_data_today = get_intraday_data('^KQ11', interval='5m', period='1d')

        merged_data_today = pd.concat([kospi_data_today, kosdaq_data_today])

        save_to_dynamodb(merged_data_today)

        log_manager.logger.info("Task3 완료")  # 작업이 완료되었음을 로그에 기록
    except Exception as e:
        log_manager.logger.error(f"Error inserting KOSPI, KOSDAQ data into DynamoDB: {e}")
        print(f"Error: {e}")


# @shared_task
# def run_task3():
#     # 한국 시간대 설정
#     # tz = pytz.timezone('Asia/Seoul')
#     # current_time = datetime.now(tz).time()

#     # # 오전 9시부터 오후 3시 20분 사이에만 실행
#     # start_time = datetime.strptime("09:00", "%H:%M").time()
#     # end_time = datetime.strptime("15:30", "%H:%M").time()

#     # if start_time <= current_time <= end_time:
#     # log_manager.logger.info("지수 데이터 DB에 저장 시작...")
#     # print("Running...")

#         # 코스피, 코스닥 5분봉 데이터 DynamoDB에 저장
#     try:
#         # 데이터 가져오기
#         log_manager.logger.info("지수 데이터 DB에 저장 시작...")
#         print("Running...")
#         kospi_data_today = get_intraday_data('^KS11', interval='5m', period='1d')
#         kosdaq_data_today = get_intraday_data('^KQ11', interval='5m', period='1d')

#         # 데이터 합치기
#         merged_data_today = pd.concat([kospi_data_today, kosdaq_data_today])

#         # DynamoDB에 저장
#         save_to_dynamodb(merged_data_today)

#     except Exception as e:
#         log_manager.logger.error(f"Error inserting KOSPI, KOSDAK data into DynamoDB: {e}")
#         # time.sleep(100)
#         # run_task3.apply_async()
#     # else:
#     #     log_manager.logger.info(f"현재 시간({current_time})은 작업 시간대가 아닙니다. 9시부터 15시 20분 사이에만 실행됩니다.")

#     # # 작업 후 100초 뒤에 다시 실행
#     # time.sleep(100)
#     # run_task3.apply_async()  # 작업이 다시 100초 후 실행되도록 Celery에 재등록
