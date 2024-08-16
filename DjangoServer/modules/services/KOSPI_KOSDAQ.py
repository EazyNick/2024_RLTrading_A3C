import yfinance as yf
import pandas as pd

import requests
import sys
import os
import boto3
from boto3.dynamodb.conditions import Key

try:
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    from utils import *
    from services import *
except ImportError:    
    from utils import *
    from services import *

def get_intraday_data(symbol, interval='5m', period='1d'):
    """
    특정 종목(symbol)의 5분봉 데이터를 가져옵니다.

    args:
    param symbol: 종목 티커 (예: '005930.KS' 삼성전자)
    param interval: 데이터 간격 (예: '5m' 5분봉)
    param period: 데이터 기간 (예: '1d' 하루)

    return: DataFrame
    """
    ticker = yf.Ticker(symbol)
    data = ticker.history(interval=interval, period=period)
    data.reset_index(inplace=True)
    data['Symbol'] = symbol  # Symbol 열 추가
    log_manager.logger.debug(f"{symbol} {period} {interval} data: {data}")
    return data


def save_to_dynamodb(data):
    # AWS DynamoDB 설정
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('kospi_kosdaq_data')

    log_manager.logger.info(f"코스피, 코스닥 5분봉 데이터 저장중...")
    """
    table.batch_writer(): DynamoDB 테이블 객체에서 batch_writer를 호출하여 배치 작성기(batch writer)를 생성 
    배치 작성기는 여러 항목을 한 번에 테이블에 넣거나 업데이트하는 데 사용
    as batch: batch_writer 객체를 batch라는 변수로 사용
    """
    with table.batch_writer() as batch:
        # data.iterrows(): 데이터프레임의 행을 반복 가능한 형태로 반환, 각 반복에서 index는 행의 인덱스를, row는 행의 데이터를 포함
        for index, row in data.iterrows():
            batch.put_item(
                Item={
                    'Timestamp': row['Datetime'].isoformat(),
                    'Symbol': row['Symbol'],
                    'Open': str(row['Open']),
                    'High': str(row['High']),
                    'Low': str(row['Low']),
                    'Close': str(row['Close']),
                    'Volume': str(row['Volume'])
                }
            )
        log_manager.logger.info(f"코스피, 코스닥 5분봉 데이터 저장 완료")

def get_kospi_kosdaq_data():
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('kospi_kosdaq_data')
    
    # 코스피 데이터를 조회 (Symbol이 '^KS11'인 항목만 조회)
    kospi_response = table.query(
        IndexName='Symbol-index',  # 인덱스 이름 (Symbol을 인덱스로 설정한 경우)
        KeyConditionExpression=Key('Symbol').eq('^KS11'),
        ProjectionExpression='Timestamp, Symbol, Close'  # 반환할 속성 지정
    )
    kospi_items = kospi_response.get('Items', [])
    
    # 코스닥 데이터를 조회 (Symbol이 '^KQ11'인 항목만 조회)
    kosdaq_response = table.query(
        IndexName='Symbol-index',  # 인덱스 이름 (Symbol을 인덱스로 설정한 경우)
        KeyConditionExpression=Key('Symbol').eq('^KQ11'),
        ProjectionExpression='Timestamp, Symbol, Close'  # 반환할 속성 지정
    )
    kosdaq_items = kosdaq_response.get('Items', [])
    
    return kospi_items, kosdaq_items

if __name__ == "__main__":
    # 코스피 지수와 코스닥 지수의 5분봉 데이터를 가져옵니다.
    kospi_data = get_intraday_data('^KS11', interval='5m', period='1d')
    kosdaq_data = get_intraday_data('^KQ11', interval='5m', period='1d')

    # 데이터 합치기
    merged_data = pd.concat([kospi_data, kosdaq_data])

    # DynamoDB에 저장
    save_to_dynamodb(merged_data)

