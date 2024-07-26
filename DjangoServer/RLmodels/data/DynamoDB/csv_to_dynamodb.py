"""
개별 실행 파일, 학습 후 테스트하는데 사용한 데이터를 가져와서, 모델의 입력에 같이 넣어주기 위해 사용
ex) 365일 데이터를 위해서는 현재 이전의 364일의 데이터가 필요하므로 불러올 필요가 있음
"""

import boto3
import csv
import os

# DynamoDB에 연결
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')  # 예: 'us-west-2'
table = dynamodb.Table('StockPrices')

# 현재 파일의 디렉토리 경로를 가져옵니다.
current_dir = os.path.dirname(os.path.abspath(__file__))

# CSV 파일의 상대 경로를 절대 경로로 변환합니다.
csv_file_path = os.path.join(current_dir, '..', '..', 'data_csv', 'kia_stock_data.csv')

# CSV 파일 읽기 및 데이터 삽입
with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # 각 행을 DynamoDB에 삽입
        table.put_item(
            Item={
                'Date': row['Date'],
                'Close': float(row['Close']),
                'Volume': int(row['Volume']),
                # 필요한 경우 다른 컬럼도 추가
                'SMA_5': float(row['SMA_5']),
                'VMA_5': float(row['VMA_5']),
                'SMA_10': float(row['SMA_10']),
                'VMA_10': float(row['VMA_10']),
                'SMA_15': float(row['SMA_15']),
                'VMA_15': float(row['VMA_15']),
                'SMA_20': float(row['SMA_20']),
                'VMA_20': float(row['VMA_20']),
                'SMA_25': float(row['SMA_25']),
                'VMA_25': float(row['VMA_25']),
                'SMA_30': float(row['SMA_30']),
                'VMA_30': float(row['VMA_30']),
                'SMA_35': float(row['SMA_35']),
                'VMA_35': float(row['VMA_35']),
                'SMA_40': float(row['SMA_40']),
                'VMA_40': float(row['VMA_40']),
                'SMA_45': float(row['SMA_45']),
                'VMA_45': float(row['VMA_45']),
                'SMA_50': float(row['SMA_50']),
                'VMA_50': float(row['VMA_50']),
                'SMA_60': float(row['SMA_60']),
                'VMA_60': float(row['VMA_60']),
                'SMA_70': float(row['SMA_70']),
                'VMA_70': float(row['VMA_70']),
                'SMA_80': float(row['SMA_80']),
                'VMA_80': float(row['VMA_80']),
                'SMA_90': float(row['SMA_90']),
                'VMA_90': float(row['VMA_90']),
                'SMA_100': float(row['SMA_100']),
                'VMA_100': float(row['VMA_100']),
                'SMA_110': float(row['SMA_110']),
                'VMA_110': float(row['VMA_110']),
                'SMA_120': float(row['SMA_120']),
                'VMA_120': float(row['VMA_120']),
                'SMA_130': float(row['SMA_130']),
                'VMA_130': float(row['VMA_130']),
                'SMA_140': float(row['SMA_140']),
                'VMA_140': float(row['VMA_140']),
                'SMA_150': float(row['SMA_150']),
                'VMA_150': float(row['VMA_150']),
                'SMA_160': float(row['SMA_160']),
                'VMA_160': float(row['VMA_160']),
                'SMA_170': float(row['SMA_170']),
                'VMA_170': float(row['VMA_170']),
                'SMA_180': float(row['SMA_180']),
                'VMA_180': float(row['VMA_180']),
                'SMA_190': float(row['SMA_190']),
                'VMA_190': float(row['VMA_190']),
                'SMA_200': float(row['SMA_200']),
                'VMA_200': float(row['VMA_200']),
                'SMA_210': float(row['SMA_210']),
                'VMA_210': float(row['VMA_210']),
                'SMA_220': float(row['SMA_220']),
                'VMA_220': float(row['VMA_220']),
                'SMA_230': float(row['SMA_230']),
                'VMA_230': float(row['VMA_230']),
                'SMA_240': float(row['SMA_240']),
                'VMA_240': float(row['VMA_240']),
                'SMA_250': float(row['SMA_250']),
                'VMA_250': float(row['VMA_250']),
                'SMA_260': float(row['SMA_260']),
                'VMA_260': float(row['VMA_260']),
                'SMA_270': float(row['SMA_270']),
                'VMA_270': float(row['VMA_270']),
                'SMA_280': float(row['SMA_280']),
                'VMA_280': float(row['VMA_280']),
                'SMA_290': float(row['SMA_290']),
                'VMA_290': float(row['VMA_290']),
                'SMA_300': float(row['SMA_300']),
                'VMA_300': float(row['VMA_300']),
                'SMA_310': float(row['SMA_310']),
                'VMA_310': float(row['VMA_310']),
                'SMA_320': float(row['SMA_320']),
                'VMA_320': float(row['VMA_320']),
                'SMA_330': float(row['SMA_330']),
                'VMA_330': float(row['VMA_330']),
                'SMA_340': float(row['SMA_340']),
                'VMA_340': float(row['VMA_340']),
                'SMA_350': float(row['SMA_350']),
                'VMA_350': float(row['VMA_350']),
                'SMA_360': float(row['SMA_360']),
                'VMA_360': float(row['VMA_360']),
                'SMA_370': float(row['SMA_370']),
                'VMA_370': float(row['VMA_370']),
                'SMA_380': float(row['SMA_380']),
                'VMA_380': float(row['VMA_380']),
                'SMA_390': float(row['SMA_390']),
                'VMA_390': float(row['VMA_390']),
                'SMA_400': float(row['SMA_400']),
                'VMA_400': float(row['VMA_400']),
                'SMA_410': float(row['SMA_410']),
                'VMA_410': float(row['VMA_410']),
                'SMA_420': float(row['SMA_420']),
                'VMA_420': float(row['VMA_420']),
                'SMA_430': float(row['SMA_430']),
                'VMA_430': float(row['VMA_430']),
                'SMA_440': float(row['SMA_440']),
                'VMA_440': float(row['VMA_440']),
                'SMA_450': float(row['SMA_450']),
                'VMA_450': float(row['VMA_450']),
                'SMA_460': float(row['SMA_460']),
                'VMA_460': float(row['VMA_460']),
                'SMA_470': float(row['SMA_470']),
                'VMA_470': float(row['VMA_470']),
                'SMA_480': float(row['SMA_480']),
                'VMA_480': float(row['VMA_480']),
                'SMA_490': float(row['SMA_490']),
                'VMA_490': float(row['VMA_490']),
                'SMA_500': float(row['SMA_500']),
                'VMA_500': float(row['VMA_500']),
                'SMA_510': float(row['SMA_510']),
                'VMA_510': float(row['VMA_510']),
                'SMA_520': float(row['SMA_520']),
                'VMA_520': float(row['VMA_520']),
                'SMA_530': float(row['SMA_530']),
                'VMA_530': float(row['VMA_530']),
                'SMA_540': float(row['SMA_540']),
                'VMA_540': float(row['VMA_540']),
                'SMA_550': float(row['SMA_550']),
                'VMA_550': float(row['VMA_550']),
                'SMA_560': float(row['SMA_560']),
                'VMA_560': float(row['VMA_560']),
                'SMA_570': float(row['SMA_570']),
                'VMA_570': float(row['VMA_570']),
                'SMA_580': float(row['SMA_580']),
                'VMA_580': float(row['VMA_580']),
                'SMA_590': float(row['SMA_590']),
                'VMA_590': float(row['VMA_590']),
                'SMA_600': float(row['SMA_600']),
                'VMA_600': float(row['VMA_600']),
                'SMA_610': float(row['SMA_610']),
                'VMA_610': float(row['VMA_610']),
                'SMA_620': float(row['SMA_620']),
                'VMA_620': float(row['VMA_620']),
                'SMA_630': float(row['SMA_630']),
                'VMA_630': float(row['VMA_630']),
                'SMA_640': float(row['SMA_640']),
                'VMA_640': float(row['VMA_640']),
                'SMA_650': float(row['SMA_650']),
                'VMA_650': float(row['VMA_650']),
                'SMA_660': float(row['SMA_660']),
                'VMA_660': float(row['VMA_660']),
                'SMA_670': float(row['SMA_670']),
                'VMA_670': float(row['VMA_670']),
                'SMA_680': float(row['SMA_680']),
                'VMA_680': float(row['VMA_680']),
                'SMA_690': float(row['SMA_690']),
                'VMA_690': float(row['VMA_690']),
                'SMA_700': float(row['SMA_700']),
                'VMA_700': float(row['VMA_700']),
                '365D_High': float(row['365D_High']),
                '365D_Low': float(row['365D_Low']),
                '180D_High': float(row['180D_High']),
                '180D_Low': float(row['180D_Low']),
                '90D_High': float(row['90D_High']),
                '90D_Low': float(row['90D_Low']),
                '30D_High': float(row['30D_High']),
                '30D_Low': float(row['30D_Low']),
                'AllTime_High': float(row['AllTime_High']),
                'AllTime_Low': float(row['AllTime_Low'])
            }
        )
        print(f"Inserted {row['Date']}")

print("Data insertion complete.")