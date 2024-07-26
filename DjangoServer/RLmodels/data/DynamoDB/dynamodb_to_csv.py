import boto3
import pandas as pd

def convert_dynamodb_to_csv():
    # DynamoDB에 연결
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')  # 예: 'us-west-2'
    table = dynamodb.Table('StockPrices')

    # DynamoDB에서 데이터 읽기
    response = table.scan()
    items = response['Items']

    # DataFrame으로 변환
    df = pd.DataFrame(items)

    exclude_keys = [
                'SMA_55', 'SMA_65', 'SMA_75', 'SMA_85', 'SMA_95', 'SMA_105', 'SMA_115', 'SMA_125', 'SMA_135', 
                'SMA_145', 'SMA_155', 'SMA_165', 'SMA_175', 'SMA_185', 'SMA_195', 'SMA_205', 'SMA_215', 'SMA_225', 
                'SMA_235', 'SMA_245', 'SMA_255', 'SMA_265', 'SMA_275', 'SMA_285', 'SMA_295', 'SMA_305', 'SMA_315', 
                'SMA_325', 'SMA_335', 'SMA_345', 'SMA_355', 'SMA_365', 'SMA_375', 'SMA_385', 'SMA_395', 'SMA_405', 
                'SMA_415', 'SMA_425', 'SMA_435', 'SMA_445', 'SMA_455', 'SMA_465', 'SMA_475', 'SMA_485', 'SMA_495', 
                'SMA_505', 'SMA_515', 'SMA_525', 'SMA_535', 'SMA_545', 'SMA_555', 'SMA_565', 'SMA_575', 'SMA_585', 
                'SMA_595', 'SMA_605', 'SMA_615', 'SMA_625', 'SMA_635', 'SMA_645', 'SMA_655', 'SMA_665', 'SMA_675', 
                'SMA_685', 'SMA_695', 'VMA_55', 'VMA_65', 'VMA_75', 'VMA_85', 'VMA_95', 'VMA_105', 'VMA_115', 
                'VMA_125', 'VMA_135', 'VMA_145', 'VMA_155', 'VMA_165', 'VMA_175', 'VMA_185', 'VMA_195', 'VMA_205', 
                'VMA_215', 'VMA_225', 'VMA_235', 'VMA_245', 'VMA_255', 'VMA_265', 'VMA_275', 'VMA_285', 'VMA_295', 
                'VMA_305', 'VMA_315', 'VMA_325', 'VMA_335', 'VMA_345', 'VMA_355', 'VMA_365', 'VMA_375', 'VMA_385', 
                'VMA_395', 'VMA_405', 'VMA_415', 'VMA_425', 'VMA_435', 'VMA_445', 'VMA_455', 'VMA_465', 'VMA_475', 
                'VMA_485', 'VMA_495', 'VMA_505', 'VMA_515', 'VMA_525', 'VMA_535', 'VMA_545', 'VMA_555', 'VMA_565', 
                'VMA_575', 'VMA_585', 'VMA_595', 'VMA_605', 'VMA_615', 'VMA_625', 'VMA_635', 'VMA_645', 'VMA_655', 
                'VMA_665', 'VMA_675', 'VMA_685', 'VMA_695'
            ]

    # 컬럼 순서 정렬 (원래 CSV 형식에 맞추기 위해)
    columns = ['Date', 'Close', 'Volume'] + \
              [f'SMA_{i}' for i in range(5, 705, 5) if f'SMA_{i}' not in exclude_keys] + \
              [f'VMA_{i}' for i in range(5, 705, 5) if f'VMA_{i}' not in exclude_keys] + \
              ['365D_High', '365D_Low', '180D_High', '180D_Low', '90D_High', '90D_Low', '30D_High', '30D_Low', 'AllTime_High', 'AllTime_Low']
    df = df[columns]

    # 필요한 데이터 타입으로 변환
    df['Close'] = df['Close'].astype(float)
    df['Volume'] = df['Volume'].astype(int)
    for i in range(5, 705, 5):
        sma_key = f'SMA_{i}'
        vma_key = f'VMA_{i}'
    
        if sma_key not in exclude_keys:
            df[sma_key] = df[sma_key].astype(float)
            
        if vma_key not in exclude_keys:
            df[vma_key] = df[vma_key].astype(float)
            
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

    print(f"Data exported to {csv_file_path}")

if __name__ == '__main__':
    convert_dynamodb_to_csv()



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
