import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import sys
import os
from pathlib import Path

# 프로젝트 루트 경로를 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

sys.path.append(str(Path(__file__).resolve().parent / 'modules'))

try:
    from Agent.A3CAgent import A3CAgent  # A3CAgent 클래스 불러오기
    from env.env import StockTradingEnv
    from modules.utils import *
except Exception as e:
    print(f"import error {e}")

# 저장된 모델을 로드하고 새 데이터를 기반으로 매수, 매도를 수행하는 함수
def run_trading(agent, env, new_data):

    # 프로젝트 루트 경로를 추가
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(project_root)

    sys.path.append(str(Path(__file__).resolve().parent / 'modules'))

    try:
        from modules.utils import log_manager
    except Exception as e:
        print(f"import error {e}")

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
    
    return account_values, stock_prices, dates, env.buy_sell_log

def plot_trading_results(dates, account_values, stock_prices, buy_sell_log):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(dates, account_values, label='Account Value', color='b')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Account Value', color='b')

    ax2 = ax1.twinx()
    ax2.plot(dates, stock_prices, label='Stock Price', color='orange', linestyle='--')
    ax2.set_ylabel('Stock Price', color='orange')

    for log in buy_sell_log:
        date, action, num_stocks, price = log
        if action == 'buy':
            ax2.scatter(date, price, color='green', marker='^', label='Buy' if 'Buy' not in ax2.get_legend_handles_labels()[1] else "")
        elif action == 'sell':
            ax2.scatter(date, price, color='red', marker='v', label='Sell' if 'Sell' not in ax2.get_legend_handles_labels()[1] else "")

    plt.title('Account Value and Stock Price Over Time')
    fig.tight_layout()

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')

    # plt.show()

    # 현재 파일의 디렉토리 가져오기
    current_dir = Path(__file__).resolve().parent

    # output 디렉토리와 파일명 설정
    save_path = current_dir / 'output' / 'trading_results.png'

    # 이미지 파일로 저장
    plt.savefig(save_path)
    plt.close()
    log_manager.logger.info(f"Trading results saved as {save_path}")

def main_run():
    
    # 프로젝트 루트 경로를 추가
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(project_root)

    sys.path.append(str(Path(__file__).resolve().parent / 'modules'))

    try:
        from Agent.A3CAgent import A3CAgent  # A3CAgent 클래스 불러오기
        from env.env import StockTradingEnv
        from modules.utils import log_manager
    except Exception as e:
        print(f"import error {e}")

    # log_manager.logger.info("Starting trading process")
    log_manager.logger.info("Starting trading process")

    # 모델 로드
    model_path = Path(__file__).resolve().parent / 'output/a3c_stock_trading_model.pth'
    file_path = Path(__file__).resolve().parent / 'data/data_csv/kia_stock_data.csv'
    df = pd.read_csv(file_path, index_col='Date', parse_dates=True)  # 주식 데이터 로드
    env = StockTradingEnv(df)  # 환경 생성
    agent = A3CAgent(env)  # 에이전트 생성
    agent.load_model(model_path)  # 학습된 모델 로드

    # 새 데이터를 기반으로 거래 수행
    # new_data = pd.read_csv(Path(__file__).resolve().parent / 'data/data_csv/kia_stock_data.csv', index_col='Date', parse_dates=True)  # 새로운 주식 데이터 로드
    new_data = pd.read_csv(Path(__file__).resolve().parent / 'data/DynamoDB/DynamoDB.csv', index_col='Date', parse_dates=True)  # 새로운 주식 데이터 로드
    account_values, stock_prices, dates, buy_sell_log = run_trading(agent, env, new_data)
    log_manager.logger.info("Starting trading End")

    # 거래 결과 플롯 및 저장
    log_manager.logger.info("시각화 시작")
    plot_trading_results(dates, account_values, stock_prices, buy_sell_log)
    log_manager.logger.info("시각화 종료")

    return buy_sell_log


if __name__ == '__main__':
    try:
        from Agent.A3CAgent import A3CAgent  # A3CAgent 클래스 불러오기
        from env.env import StockTradingEnv
        from modules.utils import *
    except Exception as e:
        print(f"import error {e}")

    buy_sell_log = main_run()
    print(f"Buy dates: {buy_sell_log}")
    log_manager.logger.info(f"Buy dates: {buy_sell_log}")
