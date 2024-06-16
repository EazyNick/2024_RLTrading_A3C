import os
import sys
from load_env import load_env_file

try:
    # 현재 파일의 경로를 기준으로 상위 디렉토리 경로를 추가
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    from utils import *
except:    
    from utils import *

import keyring

class KeyringManager:
    def __init__(self):
        # .env 파일 로드
        load_env_file('key.env')
        # 환경 변수에서 값 불러오기
        self.app_key = os.getenv('APP_KEY')
        self.app_secret_key = os.getenv('APP_SECRET_KEY')
        log_manager.logger.debug(self.app_key)
        log_manager.logger.debug(self.app_secret_key)
        self.store_keys()

    def store_keys(self):
        # 키 저장
        keyring.set_password('mock_app_key', 'Henry', self.app_key)
        keyring.set_password('mock_app_secret', 'Henry', self.app_secret_key)

# 키 저장 실행 (한번만 실행)
if __name__ == "__main__":
    KeyringManager()