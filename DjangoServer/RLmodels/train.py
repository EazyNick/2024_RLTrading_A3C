import torch
import torch.multiprocessing as mp
import pandas as pd
from Agent import A3CAgent, update_global_model
from env import StockTradingEnv

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

def worker(global_agent, env, n_episodes, global_ep, global_ep_lock, optimizer):
    """
    학습 작업자 함수

    Args:
        global_agent (A3CAgent): 글로벌 에이전트
        env (gym.Env): 환경
        n_episodes (int): 에피소드 수
        global_ep (mp.Value): 글로벌 에피소드 카운터
        global_ep_lock (mp.Lock): 에피소드 카운터 잠금
        optimizer (optim.Optimizer): 글로벌 모델의 옵티마이저
    """
    local_agent = A3CAgent(env)
    for _ in range(n_episodes):
        state = env.reset()
        states, actions, rewards, dones = [], [], [], []
        while True:
            action, _ = local_agent.select_action(state)
            next_state, reward, done, _ = env.step(action)

            states.append(state)
            actions.append(action)
            rewards.append(reward)
            dones.append(done)

            state = next_state
            if done:
                break

        trajectory = (states, actions, rewards, dones, next_state)
        local_agent.update(trajectory)  # 로컬 모델 업데이트

        # 글로벌 모델 업데이트
        optimizer.zero_grad()
        update_global_model(global_agent.model, local_agent.model, optimizer)
        
        # 이 블록 안에 있는 코드는 다른 프로세스에서 동시에 실행되지 않도록 보장(lock)
        with global_ep_lock:
            global_ep.value += 1
            log_manager.logger.info(f'Episode {global_ep.value} completed')

# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# 모델 학습 시작과 관련된 코드

def initialize_environment_and_agent(data_path):
    """
    주식 데이터를 로드하고 트레이딩 환경과 글로벌 A3C 에이전트를 초기화합니다.

    Args:
        data_path (str): 주식 데이터가 포함된 CSV 파일 경로.

    Returns:
        env (StockTradingEnv): 초기화된 트레이딩 환경.
        global_agent (A3CAgent): 초기화된 글로벌 A3C 에이전트.
        df (pd.DataFrame): 주식 데이터를 포함한 DataFrame.
    """
    # 주식 데이터를 CSV 파일에서 로드
    df = pd.read_csv(data_path)
    
    # 트레이딩 환경을 초기화
    env = StockTradingEnv(df)
    
    # 글로벌 A3C 에이전트를 초기화
    global_agent = A3CAgent(env)
    
    return env, global_agent, df


def start_training(global_agent, env, n_processes=4, n_episodes=8):
    """
    여러 프로세스를 사용하여 학습 프로세스를 시작합니다.

    Args:
        global_agent (A3CAgent): 글로벌 A3C 에이전트.
        env (StockTradingEnv): 트레이딩 환경.
        n_processes (int): 학습에 사용할 프로세스 수.
        n_episodes (int): 학습할 총 에피소드 수.
    """
    global_ep = mp.Value('i', 0)
    global_ep_lock = mp.Lock()
    optimizer = torch.optim.Adam(global_agent.model.parameters(), lr=0.001)

    processes = []
    episodes_per_process = n_episodes // n_processes
    for process_num in range(n_processes):
        p = mp.Process(target=worker, args=(global_agent, env, episodes_per_process, global_ep, global_ep_lock, optimizer))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

def save_trained_model(global_agent, model_path):
    """
    학습된 모델을 지정된 경로에 저장합니다.

    Args:
        global_agent (A3CAgent): 학습된 글로벌 A3C 에이전트.
        model_path (str): 모델을 저장할 경로.
    """
    global_agent.save_model(model_path)

if __name__ == '__main__':
    data_path = r'DjangoServer\RLmodels\data\data_csv\samsung_stock_data.csv'
    model_path = r'DjangoServer\RLmodels\output\a3c_stock_trading_model.pth'

    # 환경과 에이전트 초기화
    env, global_agent, df = initialize_environment_and_agent(data_path)

    # 학습 프로세스 시작
    start_training(global_agent, env)

    # 학습된 모델 저장
    save_trained_model(global_agent, model_path)

    log_manager.logger.info("Training process completed")
