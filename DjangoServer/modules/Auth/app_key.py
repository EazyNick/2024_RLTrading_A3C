import os
import sys
from pathlib import Path

# 현재 파일의 부모 디렉토리 경로 추가
sys.path.append(str(Path(__file__).resolve().parent))

from load_env import load_env_file

try:
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    from utils import *
except Exception as e:
    print(f"Error importing utils: {e}", file=sys.stderr)
    from utils import * 
    sys.exit(1)

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Appkey.env')
KEY_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'key_store.txt')

class KeyringManager:
    def __init__(self):
        load_env_file(PATH)
        self.__app_key = os.getenv('APP_KEY')
        self.__app_secret_key = os.getenv('APP_SECRET_KEY')

        if not self.__app_key:
            log_manager.logger.error(f"APP_KEY environment variable is missing")
            raise ValueError("APP_KEY environment variable is missing")
        if not self.__app_secret_key:
            log_manager.logger.error(f"APP_SECRET_KEY environment variable is missing")
            raise ValueError("APP_SECRET_KEY environment variable is missing")
        
        self.__app_key_changes = 0
        self.__app_secret_key_changes = 0
        self.store_keys()

    def store_keys(self):
        try:
            with open(KEY_FILE_PATH, 'w') as key_file:
                key_file.write(f"mock_app_key:EazyNick08:{self.__app_key}\n")
                key_file.write(f"mock_app_secret:EazyNick08:{self.__app_secret_key}\n")
        except Exception as e:
            log_manager.logger.error(f"Failed to store keys: {e}")
            raise

    def load_keys(self):
        try:
            with open(KEY_FILE_PATH, 'r') as key_file:
                for line in key_file:
                    if line.startswith("mock_app_key:EazyNick08:"):
                        self.__app_key = line.strip().split(":")[2]
                    elif line.startswith("mock_app_secret:EazyNick08:"):
                        self.__app_secret_key = line.strip().split(":")[2]
        except FileNotFoundError:
            log_manager.logger.warning("Key file not found, storing new keys.")
            self.store_keys()
        except Exception as e:
            log_manager.logger.error(f"Failed to load keys: {e}")
            raise

    @property
    def app_key(self):
        return self.__app_key

    @app_key.setter
    def app_key(self, value):
        if not value:
            log_manager.logger.error("App key cannot be empty")
            raise ValueError("App key cannot be empty")
        if value == self.__app_key:
            log_manager.logger.warning("New app key is the same as the current app key. No change made.")
            return
        self.__app_key_changes += 1
        if self.__app_key_changes > 2:
            log_manager.logger.error("App key has been changed more than twice.")
            raise ValueError("App key has been changed more than twice.")
        self.__app_key = value
        self.store_keys()

    @property
    def app_secret_key(self):
        return self.__app_secret_key

    @app_secret_key.setter
    def app_secret_key(self, value):
        if not value:
            raise ValueError("App secret key cannot be empty")
        if value == self.__app_secret_key:
            log_manager.logger.warning("New app secret key is the same as the current app secret key. No change made.")
            return
        self.__app_secret_key_changes += 1
        if self.__app_secret_key_changes > 2:
            raise ValueError("App secret key has been changed more than twice.")
        self.__app_secret_key = value
        self.store_keys()

# 키 저장 실행 (한번만 실행)
if __name__ == "__main__":
    keyring_manager = KeyringManager()
    keyring_manager.load_keys()
    app_key = keyring_manager.app_key
    app_secret = keyring_manager.app_secret_key

    print(app_key, app_secret)
