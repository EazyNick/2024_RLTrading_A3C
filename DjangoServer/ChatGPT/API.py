import yfinance as yf
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
    from modules.Auth import load_env_file
except Exception as e:
    print(f"import error {e}")

def get_stock_data(ticker):
    """
    기아차 주식 데이터를 가져오고 주간 및 월간 데이터를 결합한 후 반환합니다.
    
    Args:
        ticker (str): 주식 티커 심볼

    Returns:
        pd.DataFrame: 주간 및 월간 데이터가 결합된 데이터프레임
    """
    # 기아차 주식 데이터 가져오기
    stock_data = yf.Ticker(ticker)

    # 최근 1개월간 주간 단위의 과거 데이터 가져오기
    weekly_data = stock_data.history(period='1mo', interval='1wk')

    # 최근 1년간 월간 단위의 과거 데이터 가져오기
    monthly_data = stock_data.history(period='1y', interval='1mo')

    # 데이터 합치기
    combined_data = pd.concat([weekly_data, monthly_data], keys=['Weekly', 'Monthly'])

    return combined_data

def predict_stock_performance(data_str, model="gpt-3.5-turbo"):
    """
    주어진 주식 데이터를 기반으로 GPT 모델을 통해 예측 점수를 반환합니다.
    
    Args:
        data_str (str): 주식 데이터 문자열
        model (str): 사용할 GPT 모델 (기본값: "gpt-3.5-turbo")

    Returns:
        str: 예측 점수
    """

    # .env 파일에서 환경 변수 로드
    load_env_file(PATH)
    # OpenAI API 키 설정
    api_key_custom = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key_custom)

    # 프롬프트 구성
    messages = [
        {"role": "system", "content": "You are a financial assistant specialized in stock market predictions."},
        {"role": "user", "content": f"Here is the historical weekly stock data for Kia Motors for the past month including the 5-day Simple Moving Average (SMA):\n\n{data_str}\n\nBased on this data, predict the stock's future performance and provide a score between -1000 (sell) and 1000 (buy). Only return the score as a number without any additional text."}
    ]
    response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )
    
    # 응답에서 점수 추출
    prediction_score = response.choices[0].message.content
    
    return prediction_score

def API_main():
    ticker = '000270.KS'
    combined_data = get_stock_data(ticker)
    
    # 데이터의 첫 몇 줄 출력
    log_manager.logger.debug(combined_data.head())
    
    # 가져온 데이터를 문자열로 변환
    data_str = combined_data.to_string()

    # 예측 수행
    prediction_score = predict_stock_performance(data_str)
    log_manager.logger.info(f"Chat GPT Prediction Score: {prediction_score}")

if __name__ == "__main__":
    main()
