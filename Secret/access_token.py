import json

def save_access_token(access_token, file_path = 'access_token.json'):
    """access_token을 JSON 파일에 저장하는 함수"""
    data = {
        "access_token": access_token
    }
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

def load_access_token(file_path = 'access_token.json'):
    """JSON 파일에서 access_token을 불러오는 함수"""
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            # log_manager.logger.debug(data.get("access_token"))
            return data.get("access_token")
    except FileNotFoundError:
        return None

if __name__ == "__main__":
    # 액세스 토큰을 저장
    access_token = "your_access_token_here"
    save_access_token(access_token)
    
    # 저장된 액세스 토큰을 불러오기
    loaded_access_token = load_access_token()
    if loaded_access_token:
        print(f"Loaded Access Token: {loaded_access_token}")
    else:
        print("Access token file not found or empty.")