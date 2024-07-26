import pandas as pd
from Agent.A3CAgent import A3CAgent  # A3CAgent 클래스 불러오기
from env.env import StockTradingEnv
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import os
import sys

try:
    # 현재 파일의 디렉토리를 기준으로 상위 디렉토리로 이동하여 'modules' 폴더 경로를 만듭니다.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    modules_dir = os.path.abspath(os.path.join(current_dir, '../modules'))
    rlmodels_dir = os.path.abspath(os.path.join(current_dir, '..'))

    # 필요한 경로를 sys.path에 추가합니다.
    sys.path.extend([modules_dir, rlmodels_dir])

    from utils import *
    from env import *
    from models import *
except ImportError as e:
    print(f"ImportError: {e}")

# 저장된 모델을 로드하고 새 데이터를 기반으로 매수, 매도를 수행하는 함수
def run_trading(agent, env, new_data):
    state = env.reset(new_df=new_data)  # 새로운 데이터를 사용하여 환경 초기화
    done = False
    account_values = []  # 계좌 잔고 기록
    stock_prices = []  # 주식 가격 기록
    dates = []  # 날짜 기록
    
    while not done:
        action, _ = agent.select_action(state)  # 행동 선택
        next_state, reward, done, _ = env.step(action)  # 다음 상태와 보상 얻기
        state = next_state  # 상태 업데이트
        
        account_value = state[1] + state[0] * env.stock_owned  # 현금 잔고 + (보유 주식 * 주식 가격)
        account_values.append(account_value)
        stock_prices.append(state[0])  # 현재 주식 가격 기록
        dates.append(env.df.index[env.current_step])  # 날짜 기록
        
        # 추가 로그
        log_manager.logger.info(f"Step: {env.current_step}, Stock Price: {state[0]}, Account Value: {account_value}, Stocks Owned: {env.stock_owned}, Cash in Hand: {state[1]}")
        
        env.render()
    
    return account_values, stock_prices, dates

if __name__ == '__main__':
    log_manager.logger.info("Starting trading process")
    # 모델 로드
    model_path = r'DjangoServer\RLmodels\output\a3c_stock_trading_model.pth'
    df = pd.read_csv('DjangoServer\RLmodels\data\data_csv\samsung_stock_data.csv', index_col='Date', parse_dates=True)  # 주식 데이터 로드
    env = StockTradingEnv(df)  # 환경 생성
    agent = A3CAgent(env)  # 에이전트 생성
    agent.load_model(model_path)  # 학습된 모델 로드

    # 새 데이터를 기반으로 거래 수행
    new_data = pd.read_csv('DjangoServer\RLmodels\data\data_csv\samsung_stock_data.csv', index_col='Date', parse_dates=True)  # 새로운 주식 데이터 로드
    account_values, stock_prices, dates = run_trading(agent, env, new_data)
    
    # 값 정규화
    scaler = MinMaxScaler()
    account_values_scaled = scaler.fit_transform(pd.DataFrame(account_values))
    stock_prices_scaled = scaler.fit_transform(pd.DataFrame(stock_prices))

    # 결과를 그래프로 시각화
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(dates, account_values_scaled, label='Account Value', color='b')
    ax.plot(dates, stock_prices_scaled, label='Samsung Stock Price', color='orange')
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Normalized Value')
    
    plt.title('Account Value and Samsung Stock Price Over Time')
    fig.tight_layout()

    # 레전드를 왼쪽 상단에 배치
    ax.legend(loc='upper left')
    
    plt.show()