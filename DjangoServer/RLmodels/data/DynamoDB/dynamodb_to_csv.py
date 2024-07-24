import boto3
import pandas as pd

# DynamoDB에 연결
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
table = dynamodb.Table('StockPrices')

# DynamoDB에서 데이터 읽기
response = table.scan()
items = response['Items']

# DataFrame으로 변환
df = pd.DataFrame(items)

# 컬럼 순서 정렬 (원래 CSV 형식에 맞추기 위해)
columns = ['Date', 'Close', 'Volume'] + \
          [f'SMA_{i}' for i in range(5, 705, 5)] + \
          [f'VMA_{i}' for i in range(5, 705, 5)] + \
          ['365D_High', '365D_Low', '180D_High', '180D_Low', '90D_High', '90D_Low', '30D_High', '30D_Low', 'AllTime_High', 'AllTime_Low']
df = df[columns]

# 필요한 데이터 타입으로 변환
df['Close'] = df['Close'].astype(float)
df['Volume'] = df['Volume'].astype(int)
for i in range(5, 705, 5):
    df[f'SMA_{i}'] = df[f'SMA_{i}'].astype(float)
    df[f'VMA_{i}'] = df[f'VMA_{i}'].astype(float)
df['365D_High'] = df['365D_High'].astype(float)
df['365D_Low'] = df['365D_Low'].astype(float)
df['180D_High'] = df['180D_High'].astype(float)
df['180D_Low'] = df['180D_Low'].astype(float)
df['90D_High'] = df['90D_High'].astype(float)
df['90D_Low'] = df['90D_Low'].astype(float)
df['30D_High'] = df['30D_High'].astype(float)
df['30D_Low'] = df['30D_Low'].astype(float)
df['AllTime_High'] = df['AllTime_High'].astype(float)
df['AllTime_Low'] = df['AllTime_Low'].astype(float)

# CSV 파일로 저장
csv_file_path = r'DjangoServer\RLmodels\data\DynamoDB'
df.to_csv(csv_file_path, index=False)

print("Data saved to CSV file.")


"""
csv로 저장하지 않고, 바로 모델의 입력으로 넣어주는 코드
"""
# import boto3
# import pandas as pd

# # DynamoDB에 연결
# dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')  # 예: 'us-west-2'
# table = dynamodb.Table('StockPrices')

# # DynamoDB에서 데이터 읽기
# response = table.scan()
# items = response['Items']

# # DataFrame으로 변환
# df = pd.DataFrame(items)

# # 컬럼 순서 정렬 (원래 CSV 형식에 맞추기 위해)
# columns = ['Date', 'Close', 'Volume'] + \
#           [f'SMA_{i}' for i in range(5, 705, 5)] + \
#           [f'VMA_{i}' for i in range(5, 705, 5)] + \
#           ['365D_High', '365D_Low', '180D_High', '180D_Low', '90D_High', '90D_Low', '30D_High', '30D_Low', 'AllTime_High', 'AllTime_Low']
# df = df[columns]

# # 필요한 데이터 타입으로 변환
# df['Close'] = df['Close'].astype(float)
# df['Volume'] = df['Volume'].astype(int)
# for i in range(5, 705, 5):
#     df[f'SMA_{i}'] = df[f'SMA_{i}'].astype(float)
#     df[f'VMA_{i}'] = df[f'VMA_{i}'].astype(float)
# df['365D_High'] = df['365D_High'].astype(float)
# df['365D_Low'] = df['365D_Low'].astype(float)
# df['180D_High'] = df['180D_High'].astype(float)
# df['180D_Low'] = df['180D_Low'].astype(float)
# df['90D_High'] = df['90D_High'].astype(float)
# df['90D_Low'] = df['90D_Low'].astype(float)
# df['30D_High'] = df['30D_High'].astype(float)
# df['30D_Low'] = df['30D_Low'].astype(float)
# df['AllTime_High'] = df['AllTime_High'].astype(float)
# df['AllTime_Low'] = df['AllTime_Low'].astype(float)

# # A3C 모델에 입력으로 사용 (예시)
# # 이 부분은 사용자의 A3C 모델 코드에 맞추어 조정해야 합니다.
# # 예를 들어, 모델의 입력 형식에 맞게 데이터를 배열로 변환하는 작업이 필요할 수 있습니다.
# input_data = df.to_numpy()

# # 모델에 입력
# # model.predict(input_data)  # 예시, 모델의 예측 함수 호출

# print("Data transformed and ready for A3C model input.")
