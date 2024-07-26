import boto3
import csv
import os
from decimal import Decimal

# DynamoDB에 연결
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')  # 예: 'us-west-2'
table = dynamodb.Table('StockPrices')

# 테이블 스캔 및 항목 삭제
def delete_all_items(table):
    scan = table.scan()
    with table.batch_writer() as batch:
        for each in scan['Items']:
            batch.delete_item(Key={'Date': each['Date']})

delete_all_items(table)
print('All items in table StockPrices have been deleted.')

# 현재 파일의 디렉토리 경로를 가져옵니다.
current_dir = os.path.dirname(os.path.abspath(__file__))

# CSV 파일의 상대 경로를 절대 경로로 변환합니다.
csv_file_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'data', 'data_csv', 'kia_stock_testdata.csv'))

# # 경로 확인
# print(f"Current directory: {current_dir}")
# print(f"CSV file path: {csv_file_path}")

# CSV 파일이 존재하는지 확인
if not os.path.exists(csv_file_path):
    raise FileNotFoundError(f"The file at path {csv_file_path} does not exist.")

# CSV 파일 읽기 및 데이터 삽입
with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # 각 행을 DynamoDB에 삽입
        table.put_item(
            Item={
                'Date': row['Date'],
                'Close': Decimal(row['Close']),
                'Volume': int(row['Volume']),
                # 필요한 경우 다른 컬럼도 추가
                'SMA_5': Decimal(row['SMA_5']),
                'VMA_5': Decimal(row['VMA_5']),
                'SMA_10': Decimal(row['SMA_10']),
                'VMA_10': Decimal(row['VMA_10']),
                'SMA_15': Decimal(row['SMA_15']),
                'VMA_15': Decimal(row['VMA_15']),
                'SMA_20': Decimal(row['SMA_20']),
                'VMA_20': Decimal(row['VMA_20']),
                'SMA_25': Decimal(row['SMA_25']),
                'VMA_25': Decimal(row['VMA_25']),
                'SMA_30': Decimal(row['SMA_30']),
                'VMA_30': Decimal(row['VMA_30']),
                'SMA_35': Decimal(row['SMA_35']),
                'VMA_35': Decimal(row['VMA_35']),
                'SMA_40': Decimal(row['SMA_40']),
                'VMA_40': Decimal(row['VMA_40']),
                'SMA_45': Decimal(row['SMA_45']),
                'VMA_45': Decimal(row['VMA_45']),
                'SMA_50': Decimal(row['SMA_50']),
                'VMA_50': Decimal(row['VMA_50']),
                'SMA_60': Decimal(row['SMA_60']),
                'VMA_60': Decimal(row['VMA_60']),
                'SMA_70': Decimal(row['SMA_70']),
                'VMA_70': Decimal(row['VMA_70']),
                'SMA_80': Decimal(row['SMA_80']),
                'VMA_80': Decimal(row['VMA_80']),
                'SMA_90': Decimal(row['SMA_90']),
                'VMA_90': Decimal(row['VMA_90']),
                'SMA_100': Decimal(row['SMA_100']),
                'VMA_100': Decimal(row['VMA_100']),
                'SMA_110': Decimal(row['SMA_110']),
                'VMA_110': Decimal(row['VMA_110']),
                'SMA_120': Decimal(row['SMA_120']),
                'VMA_120': Decimal(row['VMA_120']),
                'SMA_130': Decimal(row['SMA_130']),
                'VMA_130': Decimal(row['VMA_130']),
                'SMA_140': Decimal(row['SMA_140']),
                'VMA_140': Decimal(row['VMA_140']),
                'SMA_150': Decimal(row['SMA_150']),
                'VMA_150': Decimal(row['VMA_150']),
                'SMA_160': Decimal(row['SMA_160']),
                'VMA_160': Decimal(row['VMA_160']),
                'SMA_170': Decimal(row['SMA_170']),
                'VMA_170': Decimal(row['VMA_170']),
                'SMA_180': Decimal(row['SMA_180']),
                'VMA_180': Decimal(row['VMA_180']),
                'SMA_190': Decimal(row['SMA_190']),
                'VMA_190': Decimal(row['VMA_190']),
                'SMA_200': Decimal(row['SMA_200']),
                'VMA_200': Decimal(row['VMA_200']),
                'SMA_210': Decimal(row['SMA_210']),
                'VMA_210': Decimal(row['VMA_210']),
                'SMA_220': Decimal(row['SMA_220']),
                'VMA_220': Decimal(row['VMA_220']),
                'SMA_230': Decimal(row['SMA_230']),
                'VMA_230': Decimal(row['VMA_230']),
                'SMA_240': Decimal(row['SMA_240']),
                'VMA_240': Decimal(row['VMA_240']),
                'SMA_250': Decimal(row['SMA_250']),
                'VMA_250': Decimal(row['VMA_250']),
                'SMA_260': Decimal(row['SMA_260']),
                'VMA_260': Decimal(row['VMA_260']),
                'SMA_270': Decimal(row['SMA_270']),
                'VMA_270': Decimal(row['VMA_270']),
                'SMA_280': Decimal(row['SMA_280']),
                'VMA_280': Decimal(row['VMA_280']),
                'SMA_290': Decimal(row['SMA_290']),
                'VMA_290': Decimal(row['VMA_290']),
                'SMA_300': Decimal(row['SMA_300']),
                'VMA_300': Decimal(row['VMA_300']),
                'SMA_310': Decimal(row['SMA_310']),
                'VMA_310': Decimal(row['VMA_310']),
                'SMA_320': Decimal(row['SMA_320']),
                'VMA_320': Decimal(row['VMA_320']),
                'SMA_330': Decimal(row['SMA_330']),
                'VMA_330': Decimal(row['VMA_330']),
                'SMA_340': Decimal(row['SMA_340']),
                'VMA_340': Decimal(row['VMA_340']),
                'SMA_350': Decimal(row['SMA_350']),
                'VMA_350': Decimal(row['VMA_350']),
                'SMA_360': Decimal(row['SMA_360']),
                'VMA_360': Decimal(row['VMA_360']),
                'SMA_370': Decimal(row['SMA_370']),
                'VMA_370': Decimal(row['VMA_370']),
                'SMA_380': Decimal(row['SMA_380']),
                'VMA_380': Decimal(row['VMA_380']),
                'SMA_390': Decimal(row['SMA_390']),
                'VMA_390': Decimal(row['VMA_390']),
                'SMA_400': Decimal(row['SMA_400']),
                'VMA_400': Decimal(row['VMA_400']),
                'SMA_410': Decimal(row['SMA_410']),
                'VMA_410': Decimal(row['VMA_410']),
                'SMA_420': Decimal(row['SMA_420']),
                'VMA_420': Decimal(row['VMA_420']),
                'SMA_430': Decimal(row['SMA_430']),
                'VMA_430': Decimal(row['VMA_430']),
                'SMA_440': Decimal(row['SMA_440']),
                'VMA_440': Decimal(row['VMA_440']),
                'SMA_450': Decimal(row['SMA_450']),
                'VMA_450': Decimal(row['VMA_450']),
                'SMA_460': Decimal(row['SMA_460']),
                'VMA_460': Decimal(row['VMA_460']),
                'SMA_470': Decimal(row['SMA_470']),
                'VMA_470': Decimal(row['VMA_470']),
                'SMA_480': Decimal(row['SMA_480']),
                'VMA_480': Decimal(row['VMA_480']),
                'SMA_490': Decimal(row['SMA_490']),
                'VMA_490': Decimal(row['VMA_490']),
                'SMA_500': Decimal(row['SMA_500']),
                'VMA_500': Decimal(row['VMA_500']),
                'SMA_510': Decimal(row['SMA_510']),
                'VMA_510': Decimal(row['VMA_510']),
                'SMA_520': Decimal(row['SMA_520']),
                'VMA_520': Decimal(row['VMA_520']),
                'SMA_530': Decimal(row['SMA_530']),
                'VMA_530': Decimal(row['VMA_530']),
                'SMA_540': Decimal(row['SMA_540']),
                'VMA_540': Decimal(row['VMA_540']),
                'SMA_550': Decimal(row['SMA_550']),
                'VMA_550': Decimal(row['VMA_550']),
                'SMA_560': Decimal(row['SMA_560']),
                'VMA_560': Decimal(row['VMA_560']),
                'SMA_570': Decimal(row['SMA_570']),
                'VMA_570': Decimal(row['VMA_570']),
                'SMA_580': Decimal(row['SMA_580']),
                'VMA_580': Decimal(row['VMA_580']),
                'SMA_590': Decimal(row['SMA_590']),
                'VMA_590': Decimal(row['VMA_590']),
                'SMA_600': Decimal(row['SMA_600']),
                'VMA_600': Decimal(row['VMA_600']),
                'SMA_610': Decimal(row['SMA_610']),
                'VMA_610': Decimal(row['VMA_610']),
                'SMA_620': Decimal(row['SMA_620']),
                'VMA_620': Decimal(row['VMA_620']),
                'SMA_630': Decimal(row['SMA_630']),
                'VMA_630': Decimal(row['VMA_630']),
                'SMA_640': Decimal(row['SMA_640']),
                'VMA_640': Decimal(row['VMA_640']),
                'SMA_650': Decimal(row['SMA_650']),
                'VMA_650': Decimal(row['VMA_650']),
                'SMA_660': Decimal(row['SMA_660']),
                'VMA_660': Decimal(row['VMA_660']),
                'SMA_670': Decimal(row['SMA_670']),
                'VMA_670': Decimal(row['VMA_670']),
                'SMA_680': Decimal(row['SMA_680']),
                'VMA_680': Decimal(row['VMA_680']),
                'SMA_690': Decimal(row['SMA_690']),
                'VMA_690': Decimal(row['VMA_690']),
                'SMA_700': Decimal(row['SMA_700']),
                'VMA_700': Decimal(row['VMA_700']),
                '365D_High': Decimal(row['365D_High']),
                '365D_Low': Decimal(row['365D_Low']),
                '180D_High': Decimal(row['180D_High']),
                '180D_Low': Decimal(row['180D_Low']),
                '90D_High': Decimal(row['90D_High']),
                '90D_Low': Decimal(row['90D_Low']),
                '30D_High': Decimal(row['30D_High']),
                '30D_Low': Decimal(row['30D_Low']),
                'AllTime_High': Decimal(row['AllTime_High']),
                'AllTime_Low': Decimal(row['AllTime_Low'])
            }
        )
        print(f"Inserted {row['Date']}")

print("Data insertion complete.")
