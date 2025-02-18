import gym
from gym import spaces
import numpy as np
import pandas as pd
import os
import sys
import random

try:
    # 현재 파일의 디렉토리를 기준으로 상위 디렉토리로 이동하여 'modules' 폴더 경로를 만듭니다.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    modules_dir = os.path.abspath(os.path.join(current_dir, '../../modules'))
    rlmodels_dir = os.path.abspath(os.path.join(current_dir, '..'))

    # 필요한 경로를 sys.path에 추가합니다.
    sys.path.extend([modules_dir, rlmodels_dir])

    from utils import *
    from config import *
except ImportError as e:
    print(f"ImportError: {e}")

# 시드값 설정 함수
def set_seeds(random_seed=None, numpy_seed=None):
    """
    모든 난수 생성기의 시드값을 각각 설정하여 일관된 결과를 생성합니다.

    Args:
        random_seed (int, optional): Python random 모듈의 시드값
        numpy_seed (int, optional): NumPy 모듈의 시드값
    """
    if random_seed is not None:
        random.seed(random_seed)

    if numpy_seed is not None:
        np.random.seed(numpy_seed)

class StockTradingEnv(gym.Env):
    def __init__(self, df, max_stock=200, trading_charge=0.00015, trading_tax=0.002):
        """
        주식 데이터프레임 df를 입력으로 받아 환경을 초기화

        Args:
            df (pd.DataFrame): 주식 데이터프레임
        """
        super(StockTradingEnv, self).__init__()

        # 시드값 설정 (각각의 시드값을 다르게 설정)
        random_seed_value = 168293 
        numpy_seed_value = 168293 
        set_seeds(random_seed=random_seed_value, numpy_seed=numpy_seed_value)
        
        log_manager.logger.info(f"StockTradingEnv initialized")

        # account_info = DataParser.get_account_info()
        # stock_info_list = DataParser.get_stock_info_list()

        # log_manager.logger.debug(f"account_info: {account_info}")
        # log_manager.logger.debug(f"stock_info_list: {stock_info_list}")

        self.df = df
        self.current_step = 0
        self.cash_in_hand = 10000000  # 초기 현금
        # self.cash_in_hand = account_info.get_total_cash_balance()  # 초기 현금
        log_manager.logger.debug(f"cash_in_hand: {self.cash_in_hand}")
        # 가장 많은 주식을 보유한 주식의 보유량을 찾습니다.
        # if stock_info_list:
        #     self.stock_owned = max(stock_info_list, key=lambda x: x.get_holding_quantity()).get_holding_quantity()
        # else:
        #     self.stock_owned = 0  # 주식이 없으면 0으로 설정
        self.stock_owned = 0 
        log_manager.logger.debug(f"stock_owned: {self.stock_owned}")
        self.max_stock = max_stock  # 한 번에 매수 또는 매도할 수 있는 최대 주식 수
        self.trading_charge = trading_charge  # 거래 수수료
        self.trading_tax = trading_tax  # 거래세

        # 행동: 0~(2*max_stock) (매도 0~max_stock, 유지 max_stock, 매수 max_stock+1~2*max_stock)
        self.action_space = spaces.Discrete(2 * max_stock + 1)
        # log_manager.logger.info(f"Action space: {self.action_space}")

        # 관찰 공간 정의
        num_sma = len([col for col in df.columns if 'SMA' in col])  # 이동평균선의 개수
        num_vma = len([col for col in df.columns if 'VMA' in col])
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(num_sma + num_vma + 2,), dtype=np.float32)
        # log_manager.logger.info(f"Observation space: {self.observation_space}")

        # 매수/매도 기록을 위한 리스트 초기화
        self.buy_sell_log = []

    def reset(self, new_df=None):
        """
        환경을 초기 상태로 재설정
        
        Args:
            new_df (pd.DataFrame, optional): 새로운 주식 데이터프레임. 제공되지 않으면 기존 데이터프레임을 사용.
        
        Returns:
            np.ndarray: 초기 관찰값
        """
        # log_manager.logger.info(f"Environment reset start")
        self.current_step = 0
        self.cash_in_hand = 10000000  # 초기 현금
        self.stock_owned = 0  # 초기 주식 보유량
        if new_df is not None:
            self.df = new_df
            log_manager.logger.info(f"New data frame provided")
        initial_observation = self._next_observation()
        # log_manager.logger.debug(f"Initial observation: {initial_observation}")
        self.buy_sell_log = []  # 매수/매도 기록 초기화
        return initial_observation

    def _next_observation(self):
        """
        현재 주식 가격(df['Close'])과 현금 잔고를 포함한 관찰값을 반환
        
        Returns:
            np.ndarray: 현재 관찰값
        """
        sma_values = self.df.iloc[self.current_step].filter(like='SMA').values
        vma_values = self.df.iloc[self.current_step].filter(like='VMA').values
        current_price = self.df['Close'].values[self.current_step]
        next_observation = np.concatenate(([current_price, self.cash_in_hand], sma_values, vma_values)).astype(np.float32)
        next_observation = np.nan_to_num(next_observation, nan=0.0)  # NaN 값을 0으로 대체
        # log_manager.logger.debug(f"Next observation: {next_observation}, current_price: {current_price}")
        return next_observation

    def step(self, action):
        """
        주어진 행동(action)에 따라 환경의 상태를 업데이트
        
        Args:
            action (int): 에이전트가 선택한 행동 (0: 매수, 1: 매도, 2: 유지)
        
        Returns:
            tuple: 다음 관찰값, 보상, 에피소드 종료 여부, 추가 정보
        """
        # log_manager.logger.info(f"Step {self.current_step}, Action: {action}")
        current_price = self.df['Close'].values[self.current_step]
        # log_manager.logger.debug(f"Current price: {current_price}")

       # 행동 정의
        # 매도
        if action < self.max_stock:
            num_stocks_to_sell = action
            if self.stock_owned >= num_stocks_to_sell:
                self.stock_owned -= num_stocks_to_sell
                self.cash_in_hand += num_stocks_to_sell * current_price * (1 - self.trading_charge - self.trading_tax)
                # log_manager.logger.info(f"Action: Sell {num_stocks_to_sell} stocks")
                self.buy_sell_log.append((self.df.index[self.current_step], 'sell', num_stocks_to_sell, current_price))
            else:
                # 보유 주식이 충분하지 않으면 매도하지 않음
                num_stocks_to_sell = 0
                # log_manager.logger.info(f"Action: Sell failed due to insufficient stock")
        # 관망
        elif action == self.max_stock:
            pass
            # log_manager.logger.info(f"Action: Hold")
        # 매수
        else:
            num_stocks_to_buy = action - self.max_stock
            cost = num_stocks_to_buy * current_price * (1 + self.trading_charge)
            if self.cash_in_hand >= cost:
                self.stock_owned += num_stocks_to_buy
                self.cash_in_hand -= cost
                # log_manager.logger.info(f"Action: Buy {num_stocks_to_buy} stocks")
                self.buy_sell_log.append((self.df.index[self.current_step], 'buy', num_stocks_to_buy, current_price))
            else:
                # 현금이 충분하지 않으면 매수하지 않음
                num_stocks_to_buy = 0
                # log_manager.logger.info(f"Action: Buy failed due to insufficient cash")

        # log_manager.logger.debug(f"Stock owned: {self.stock_owned}, Cash in hand: {self.cash_in_hand}")

        self.current_step += 1
        done = self.current_step >= len(self.df) - 1
        # log_manager.logger.debug(f"done {done}")
        # if done:
        #     log_manager.logger.info(f"Episode finished")

        reward = self.stock_owned * current_price + self.cash_in_hand
        # log_manager.logger.debug(f"Reward: {reward}")

        next_observation = self._next_observation()
        # log_manager.logger.debug(f"Next observation: {next_observation}")

        return next_observation, reward, done, {}

    def render(self, mode='human', close=False):
        """
        현재 시간 스텝과 총 수익을 출력
        
        Args:
            mode (str): 출력 모드. 'human'은 콘솔 출력.
            close (bool): 환경을 닫을지 여부. 기본값은 False.
        """
        profit = self.stock_owned * self.df['Close'].values[self.current_step] + self.cash_in_hand - 10000000
        # log_manager.logger.info(f"Profit: {profit}")

        if mode == 'human':
            log_manager.logger.info(f'Step: {self.current_step}, Profit: {profit}')
        else:
            raise NotImplementedError(f"Render mode '{mode}' is not supported.")

if __name__ == "__main__":
    data = {
        'ctx_area_fk100': ' ',
        'ctx_area_nk100': ' ',
        'output1': [
            {
                'pdno': '005930',
                'prdt_name': '삼성전자',
                'trad_dvsn_name': '현금',
                'bfdy_buy_qty': '0',
                'bfdy_sll_qty': '0',
                'thdt_buyqty': '0',
                'thdt_sll_qty': '0',
                'hldg_qty': '2',
                'ord_psbl_qty': '2',
                'pchs_avg_pric': '80750.0000',
                'pchs_amt': '161500',
                'prpr': '87100',
                'evlu_amt': '174200',
                'evlu_pfls_amt': '12700',
                'evlu_pfls_rt': '7.86',
                'evlu_erng_rt': '7.86377709',
                'loan_dt': '',
                'loan_amt': '0',
                'stln_slng_chgs': '0',
                'expd_dt': '',
                'fltt_rt': '2.96000000',
                'bfdy_cprs_icdc': '2500',
                'item_mgna_rt_name': '20%',
                'grta_rt_name': '',
                'sbst_pric': '0',
                'stck_loan_unpr': '0.0000'
            }
        ],
        'output2': [
            {
                'dnca_tot_amt': '9838480',
                'nxdy_excc_amt': '9838480',
                'prvs_rcdl_excc_amt': '9838480',
                'cma_evlu_amt': '0',
                'bfdy_buy_amt': '0',
                'thdt_buy_amt': '0',
                'nxdy_auto_rdpt_amt': '0',
                'bfdy_sll_amt': '0',
                'thdt_sll_amt': '0',
                'd2_auto_rdpt_amt': '0',
                'bfdy_tlex_amt': '0',
                'thdt_tlex_amt': '0',
                'tot_loan_amt': '0',
                'scts_evlu_amt': '174200',
                'tot_evlu_amt': '10012680',
                'nass_amt': '10012680',
                'fncg_gld_auto_rdpt_yn': '',
                'pchs_amt_smtl_amt': '161500',
                'evlu_amt_smtl_amt': '174200',
                'evlu_pfls_smtl_amt': '12700',
                'tot_stln_slng_chgs': '0',
                'bfdy_tot_asst_evlu_amt': '10007680',
                'asst_icdc_amt': '5000',
                'asst_icdc_erng_rt': '0.04996163'
            }
        ],
        'rt_cd': '0',
        'msg_cd': '20310000',
        'msg1': '모의투자 조회가 완료되었습니다.'
    }

    DataParser.parse_account_data(data)

    stock_info_list = DataParser.get_stock_info_list()
    account_info = DataParser.get_account_info()
    
    df = {0}
    test = StockTradingEnv(df)