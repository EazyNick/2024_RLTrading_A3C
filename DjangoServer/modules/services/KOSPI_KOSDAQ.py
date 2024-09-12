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

def get_previous_trading_day(symbol, interval='5m'):
    """
    전날 데이터를 가져옵니다. 만약 전날이 휴일이거나 비거래일이면, 마지막 거래일 데이터를 가져옵니다.
    """
    prev_day = datetime.now() - timedelta(1)

    while True:
        # 이틀 전부터 오늘까지의 데이터를 가져옵니다.
        data = get_intraday_data(symbol, interval=interval, period='2d')

        # 플래그 변수를 추가하여 경고 로그가 한 번만 출력되도록 함
        warning_logged = False

        if not data.empty:
            prev_day_data = data.iloc[:-len(get_intraday_data(symbol, interval=interval, period='1d'))]
            if not prev_day_data.empty:
                return prev_day_data

        prev_day -= timedelta(1)
        if prev_day.weekday() >= 5:  # 주말은 건너뜁니다.
            continue
        log_manager.logger.debug(f"이전 거래일 확인 중: {prev_day.strftime('%Y-%m-%d')}")

def save_to_dynamodb(data):
    # AWS DynamoDB 설정
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('kospi_kosdaq_data')

    log_manager.logger.info(f"코스피, 코스닥 5분봉 데이터 저장중...")
    
    for index, row in data.iterrows():
        item = {
            'Timestamp': row['Datetime'].isoformat(),
            'Symbol': row['Symbol'],
            'Open': str(row['Open']),
            'High': str(row['High']),
            'Low': str(row['Low']),
            'Close': str(row['Close']),
            'Volume': str(row['Volume'])
        }

        # log_manager.logger.debug(f"Saving item: {item}")

        try:
            response = table.put_item(
                Item=item,
                ConditionExpression="attribute_not_exists(#ts) AND attribute_not_exists(#sym)",
                ExpressionAttributeNames={
                    '#ts': 'Timestamp',
                    '#sym': 'Symbol'
                }
            )
            log_manager.logger.debug(f"Successfully saved item with Timestamp: {item['Timestamp']} and Symbol: {item['Symbol']}")
        except boto3.exceptions.botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                if not warning_logged:
                    log_manager.logger.warning(f"Item already exists, skipping insertion: {e}")
                    warning_logged = True
            else:
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

