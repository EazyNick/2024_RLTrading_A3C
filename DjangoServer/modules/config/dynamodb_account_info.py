import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from config.account_info import DataParser
from Auth import AccessTokenManager, KeyringManager
from services import get_account_balance
from utils.Logger import log_manager

class DynamoDBManager:
    @staticmethod
    def save_to_dynamodb(account_id, stock_info_list, account_info):
        """
        DynamoDB에 계좌 정보 및 주식 정보를 저장하는 함수

        Args:
            account_id (str): 계좌 ID
            stock_info_list (list): 주식 정보 객체 리스트
            account_info (DataParser.AccountInfo): 계좌 정보 객체

        Returns:
            None
        """
        try:
            dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
            table = dynamodb.Table('Accounts')
            
            stock_info_dicts = [stock.to_dict() for stock in stock_info_list]
            account_info_dict = account_info.to_dict()

            item = {
                'account_id': account_id,
                'stock_info_list': stock_info_dicts,
                'account_info': account_info_dict
            }

            table.put_item(Item=item)
            log_manager.logger.info(f"Data for account_id {account_id} saved to DynamoDB")
        except (NoCredentialsError, PartialCredentialsError) as e:
            log_manager.logger.error(f"Credential error: {e}")
        except Exception as e:
            log_manager.logger.error(f"An error occurred while saving data to DynamoDB: {e}")

    @staticmethod
    def load_from_dynamodb(account_id):
        """
        DynamoDB에서 계좌 정보 및 주식 정보를 불러오는 함수

        Args:
            account_id (str): 계좌 ID

        Returns:
            tuple: (주식 정보 객체 리스트, 계좌 정보 객체)
        """
        try:
            dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
            table = dynamodb.Table('Accounts')

            response = table.get_item(Key={'account_id': account_id})
            item = response.get('Item', None)

            if item:
                stock_info_data = item['stock_info_list']
                account_info_data = item['account_info']

                stock_info_list = [DataParser.StockInfo(stock) for stock in stock_info_data]
                account_info = DataParser.AccountInfo(account_info_data)
                log_manager.logger.info(f"Data for account_id {account_id} loaded from DynamoDB")
                return stock_info_list, account_info
            else:
                log_manager.logger.error(f"No data found for account_id: {account_id}")
                raise ValueError(f"No data found for account_id: {account_id}")
        except (NoCredentialsError, PartialCredentialsError) as e:
            log_manager.logger.error(f"Credential error: {e}")
        except Exception as e:
            log_manager.logger.error(f"An error occurred while loading data from DynamoDB: {e}")
            return None, None

# 사용 예제
if __name__ == "__main__":
    try:
        # Access token, app key, app secret 설정
        manager = AccessTokenManager()
        access_token = manager.load_access_token()
        if access_token is None:
            access_token = manager.get_access_token()
        key = KeyringManager()
        app_key = key.app_key
        app_secret = key.app_secret_key

        # 계좌 정보 불러오기
        stock_info_list, account_info = get_account_balance(access_token, app_key, app_secret)

        # DynamoDB에 저장
        account_id = "12345678"  # 예시 계좌 ID
        DataParser.parse_account_data({'output1': [stock_info.to_dict() for stock_info in stock_info_list],
                                       'output2': [account_info.to_dict()]})
        DynamoDBManager.save_to_dynamodb(account_id, stock_info_list, account_info)

        # DynamoDB에서 불러오기
        loaded_stock_info_list, loaded_account_info = DynamoDBManager.load_from_dynamodb(account_id)

        # 불러온 정보 출력
        formatter = AccountFormatter()
        formatter.format(loaded_stock_info_list, loaded_account_info)
    except Exception as e:
        log_manager.logger.error(f"An error occurred in the main process: {e}")
