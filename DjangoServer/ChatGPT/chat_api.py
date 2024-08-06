import pandas as pd
from pathlib import Path
import sys
import os
from openai import OpenAI
from dotenv import load_dotenv

# 프로젝트 루트 경로를 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'apikey.env')
sys.path.append(str(Path(__file__).resolve().parent / 'modules'))

try:
    from modules.utils import *
except Exception as e:
    print(f"import error {e}")

# 환경 변수 파일 경로 설정
PATH = 'apikey.env'

def load_env_file(env_path):
    load_dotenv(env_path)

def read_excel(file_path):
    """
    엑셀 파일을 읽어와 내용을 문자열로 반환합니다.

    Args:
        file_path (str): 엑셀 파일 경로

    Returns:
        str: 엑셀 파일 내용 문자열
    """
    df = pd.read_excel(file_path)
    content = df.to_string(index=False)
    return content

def chatgpt(user_input, document_content, model="gpt-3.5-turbo"):
    """
    자동매매 애플리케이션 chatbot 대화 함수
    
    Args:
        user_input (str): 사용자 입력 데이터 문자열
        document_content (str): 문서 내용 문자열
        model (str): 사용할 GPT 모델 (기본값: "gpt-3.5-turbo")

    Returns:
        str: 답변 메시지
    """
    
    # .env 파일에서 환경 변수 로드
    load_env_file(PATH)

    # OpenAI API 키 설정
    api_key_custom = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key_custom)

    # 프롬프트 구성
    messages = [
        {"role": "system", "content": "You are an advisor in a stock auto-trading application."},
        {"role": "user", "content": f"Document content: {document_content}"},
        {"role": "user", "content": f"User's question: {user_input}"}
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )
        review = response.choices[0].message.content
        return review
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None    

if __name__ == "__main__":
    excel_path = 'test.xlsx'
    excel_content = read_excel(excel_path)
    # user_question = '애플리케이션 서비스는 뭐가 있어?'
    user_question = '수행단계 별 산출물 작성목록에서 필수인 항목을 알려줘'

    print(chatgpt(user_question, excel_content))