import torch
import torch.nn as nn
from utils import log_manager

# 시드값 설정 함수
def set_seeds(torch_seed=None):
    """
    모든 난수 생성기의 시드값을 각각 설정하여 일관된 결과를 생성합니다.

    Args:
        torch_seed (int, optional): PyTorch 모듈의 시드값
    """

    if torch_seed is not None:
        torch.manual_seed(torch_seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(torch_seed)

class ActorCritic(nn.Module):
    def __init__(self, input_dim, action_space):
        """
        Actor-Critic 모델 초기화
        정책 그라디언트 방법과 TD 방법을 결합한 Actor-Critic 구조
        A3C에서 사용

        Args:
            input_dim (int): 입력 차원
            action_space (int): 행동 공간의 크기

        [입력층]                [은닉층]                  [출력층]
        (input_dim)  ->   (128개의 은닉 노드)  ->  (policy: action_space) 
                                              ->  (value: 1)
        """
        super(ActorCritic, self).__init__()

        # 시드값 설정 (각각의 시드값을 다르게 설정)
        torch_seed_value = 168293

        set_seeds(torch_seed=torch_seed_value)

        log_manager.logger.info("Initializing ActorCritic model")
        
        self.fc = nn.Linear(input_dim, 256) # 입력층 -> 은닉층
        # 정책 업데이트 (Actor)
        self.policy = nn.Linear(256, action_space)  # 은닉층 -> 정책 (행동)
        # 가치 업데이트 (Critic)
        self.value = nn.Linear(256, 1)  # 은닉층 -> 가치 (상태 가치)

    def forward(self, x):
        """
        전방향 신경망 연산 수행
        상태(x)를 입력으로 받아 정책(policy)과 가치(value)를 출력

        Args:
            x (torch.Tensor): 입력 텐서

        Returns:
            tuple: 정책과 가치
        """
        # log_manager.logger.debug("ActorCritic forward ...")
        x = torch.relu(self.fc(x))  # 은닉층 활성화 함수로 ReLU 사용
        policy = self.policy(x)  # 행동 확률 분포
        value = self.value(x)  # 상태 가치
        return policy, value
