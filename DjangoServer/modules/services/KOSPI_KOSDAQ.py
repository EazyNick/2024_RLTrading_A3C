import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
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
    
    # batch_writer를 사용하지 않고 각 항목을 개별적으로 삽입
    for index, row in data.iterrows():
        try:
            table.put_item(
                Item={
                    'Timestamp': row['Datetime'].isoformat(),
                    'Symbol': row['Symbol'],
                    'Open': str(row['Open']),
                    'High': str(row['High']),
                    'Low': str(row['Low']),
                    'Close': str(row['Close']),
                    'Volume': str(row['Volume'])
                },
                ConditionExpression="attribute_not_exists(Timestamp) AND attribute_not_exists(Symbol)"
                # 위 조건에 따라 동일한 Timestamp와 Symbol을 가진 항목이 없을 경우에만 삽입
            )
        except Exception as e:
            log_manager.logger.error(f"Error inserting item: {e}")

    log_manager.logger.info(f"코스피, 코스닥 5분봉 데이터 저장 완료")


def get_kospi_kosdaq_data():
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('kospi_kosdaq_data')
    
    today = datetime.now().date()
    
    # 오늘 날짜 데이터 모두 조회
    def get_today_data(symbol):
        response = table.query(
            IndexName='Symbol-Timestamp-index',
            KeyConditionExpression=Key('Symbol').eq(symbol) & Key('Timestamp').begins_with(str(today)),
            ProjectionExpression='#ts, Symbol, #cl',
            ExpressionAttributeNames={'#ts': 'Timestamp', '#cl': 'Close'}
        )
        return response.get('Items', [])
    
    # 오늘 제외한 최신 데이터 1개만 조회
    def get_latest_data_exclude_today(symbol):
        response = table.query(
            IndexName='Symbol-Timestamp-index',
            KeyConditionExpression=Key('Symbol').eq(symbol) & Key('Timestamp').lt(str(today)),
            ScanIndexForward=False,  # 가장 최신의 데이터가 우선
            Limit=1,  # 최신 데이터 1개만 가져오기
            ProjectionExpression='#ts, Symbol, #cl',
            ExpressionAttributeNames={'#ts': 'Timestamp', '#cl': 'Close'}
        )
        return response.get('Items', [])
    
    # 코스피 데이터 조회
    kospi_today = get_today_data('^KS11')
    kospi_latest = get_latest_data_exclude_today('^KS11')

    # 코스닥 데이터 조회
    kosdaq_today = get_today_data('^KQ11')
    kosdaq_latest = get_latest_data_exclude_today('^KQ11')
    
    return kospi_today, kospi_latest, kosdaq_today, kosdaq_latest

if __name__ == "__main__":
    # 코스피 지수와 코스닥 지수의 5분봉 데이터를 가져옵니다.
    kospi_data = get_intraday_data('^KS11', interval='5m', period='1d')
    kosdaq_data = get_intraday_data('^KQ11', interval='5m', period='1d')

    # 데이터 합치기
    merged_data = pd.concat([kospi_data, kosdaq_data])

    # DynamoDB에 저장
    save_to_dynamodb(merged_data)

