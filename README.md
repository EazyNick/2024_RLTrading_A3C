# 🤖 A3C 기반 주식 자동매매 시스템 (Stock Auto Trading System)

> **2024 한이음 ICT 프로젝트** | **총장배소프트웨어대회 은상** 수상작

A3C(Asynchronous Advantage Actor-Critic) 강화학습 알고리즘을 활용한 주식 자동매매 시스템입니다. Django 백엔드와 한국투자증권 REST API를 연동하여 실시간 주식 거래를 자동화하고, AWS 클라우드 환경에서 안정적으로 운영됩니다.

## 🎬 시연 영상

- **데모 영상**: [**주식 자동매매 시스템 시연 영상**](https://www.youtube.com/watch?v=ztcIzkfpueM) 🎥 - 프로젝트 기능 시연

## 👥 팀원 소개

| 역할     | 이름     | 담당 업무                       | 소속 대학교 및 학과                      |
| -------- | -------- | ------------------------------- | ---------------------------------------- |
| **팀장** | [여의주] | 프로젝트 총괄                   | [서울과학기술대학교 스마트ICT융합공학과] |
| **팀원** | [김성준] | 백엔드 개발, 강화학습 모델 구현 | [한국방송통신대학교 컴퓨터과학과]        |
| **팀원** | [고수민] | AI/ML 알고리즘 개발             | [동덕여자대학교 데이터사이언스전공]      |
| **팀원** | [최민경] | 프론트엔드 개발, API 연동       | [서울여자대학교 경제학과]                |
| **멘토** | [이규영] | 프로젝트 멘토링                 | [한국과학기술원 정보보호대학원]          |

## 🎯 프로젝트 개요

본 프로젝트는 A3C 강화학습 알고리즘을 활용하여 주식 시장에서 자동으로 매매 결정을 내리는 시스템입니다. Django 백엔드와 한국투자증권 REST API를 연동하여 실시간 주식 데이터를 수집하고, 학습된 AI 모델이 매수/매도/관망 행동을 결정하여 자동으로 거래를 실행합니다. Flutter 모바일 앱을 통해 사용자에게 직관적인 인터페이스를 제공합니다.

### 📱 프론트엔드 저장소

- **Flutter 모바일 앱**: [**stock_auto_trader**](https://github.com/EazyNick/stock_auto_trader) - 크로스 플랫폼 모바일 애플리케이션

### 🤖 AI 모델 학습 레포지토리

- **모델 학습 저장소**: [ICTRLT](https://github.com/EazyNick/ICTRLT)
- **기술 스택**: A3C 강화학습, PyTorch, Python
- **설명**: A3C(Asynchronous Advantage Actor-Critic) 강화학습 알고리즘을 활용한 주식 자동매매 모델 학습

### 🏆 주요 성과

- **2024 한이음 ICT 프로젝트** 참여
- **2024 한이음 ICT 학술발표대회** 논문 발표
- **총장배소프트웨어대회 은상** 수상

## 📚 프로젝트 자료

### 📄 논문 및 연구 자료

- **최종 논문**: [**A3C 기반 딥러닝 강화학습을 활용한 주식 자동매매 시스템 구현**](docs/papers/final/The%20Implementation%20of%20an%20Automated%20Stock%20Trading%20System%20based%20on%20A3C%20using%20Deep%20Reinforcement%20Learning.pdf) 📄
- **논문 발표 자료**: [`docs/papers/final/presentation/`](docs/papers/final/presentation/) - 논문 발표 PPT 및 학회 발표 자료

### 📊 설계서 및 문서

- **유즈케이스**: [`docs/reports/usecase/`](docs/reports/usecase/) - 시스템 유즈케이스 정의서
- **WBS**: [`docs/reports/wbs/`](docs/reports/wbs/) - 프로젝트 작업 분해 구조
- **기술 문서**: [`docs/reports/technical/`](docs/reports/technical/) - 한이음 ICT 멘토링 보고서 및 설계서
- **참고자료**: [`docs/reports/references/`](docs/reports/references/) - 강화학습, 시계열예측 등 참고 자료

## 🛠 기술 스택

### Backend

- **Python 3.9+** - 메인 프로그래밍 언어
- **Django 4.2.13** - 웹 프레임워크
- **PyTorch** - 딥러닝 프레임워크
- **Pandas** - 데이터 처리 및 분석
- **NumPy** - 수치 계산

### AI/ML

- **A3C (Asynchronous Advantage Actor-Critic)** - 강화학습 알고리즘
- **Actor-Critic 네트워크** - 정책 및 가치 함수 학습
- **Gym** - 강화학습 환경 인터페이스
- **Pandas** - 데이터 처리 및 분석
- **NumPy** - 수치 계산
- **Scikit-learn** - 머신러닝 유틸리티
- **Matplotlib** - 데이터 시각화

### Cloud & Infrastructure

- **AWS EC2** - 클라우드 서버 (Amazon Linux 2)
- **AWS DynamoDB** - NoSQL 데이터베이스
- **Nginx** - 웹 서버 및 리버스 프록시
- **Docker & Docker Compose** - 컨테이너화
- **Redis** - 메시지 브로커 및 캐시
- **Celery** - 비동기 작업 처리
- **Let's Encrypt** - SSL 인증서

### External APIs

- **한국투자증권 REST API** - 주식 거래 및 데이터 조회
- **OpenAI GPT API** - AI 챗봇 서비스
- **AWS SDK (boto3)** - 클라우드 서비스 연동
- **YFinance** - 주식 데이터 수집

### Development Tools

- **Git** - 버전 관리
- **Docker Compose** - 멀티 컨테이너 오케스트레이션
- **SSL/TLS** - 보안 통신
- **CSRF Token** - 보안 인증

## 🚀 주요 기능

### 1. 🤖 A3C 강화학습 자동매매

- **실시간 의사결정**: 주식 시장 데이터를 실시간으로 분석하여 매수/매도/관망 결정
- **Actor-Critic 구조**: 정책 네트워크(Actor)와 가치 네트워크(Critic)를 통한 효율적 학습
- **비동기 학습**: 여러 환경에서 동시에 학습하여 안정적인 수렴
- **리스크 관리**: 입실론 탐욕 정책을 통한 탐험과 활용의 균형
- **Celery 스케줄링**: 4시간마다 자동매매 실행

### 2. 📊 실시간 주식 데이터 처리

- **KOSPI/KOSDAQ** 실시간 데이터 수집
- **시계열 데이터 전처리** 및 정규화
- **기술적 지표** 계산 (SMA, VMA 등)
- **데이터 시각화** 및 결과 분석 (Matplotlib)

### 3. 💰 한국투자증권 API 연동

- **실시간 주식 가격** 조회
- **계좌 잔고** 및 보유 종목 조회
- **자동 매수/매도** 주문 실행
- **거래 내역** 기록 및 관리
- **API 키 관리** 및 토큰 갱신

### 4. 🔐 보안 및 인증 시스템

- **API 키 관리** 및 암호화 (Keyring)
- **CSRF 토큰** 보안
- **JWT 토큰** 인증
- **HTTPS** 통신 암호화 (Let's Encrypt)
- **CORS** 설정

### 5. 🤖 AI 챗봇 상담

- **OpenAI GPT** 기반 투자 상담
- **실시간 질의응답** 시스템
- **투자 전략** 조언 및 분석
- **과매수 구간 감지** (900점 이상)

### 6. ☁️ 클라우드 인프라

- **AWS EC2** 서버 운영 (Amazon Linux 2)
- **DynamoDB** 데이터 저장
- **Redis** 메시지 브로커
- **Docker** 컨테이너화
- **Nginx** 리버스 프록시

## 🏗 시스템 아키텍처

```
                       ┌─────────────────┐
                       │   OpenAI GPT    │
                       │   API           │
                       └─────────────────┘
                                ▲
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django        │    │   A3C Agent     │
│   (Web/Mobile)  │◄──►│   Backend       │◄──►│   (PyTorch)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                ▲                        │
                                │                        ▼
                                │               ┌─────────────────┐
                                │               │   AWS DynamoDB  │
                                │               │   (데이터 저장)  │
                                │               └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   한국투자증권   │
                       │   REST API      │
                       └─────────────────┘
```

## 📁 프로젝트 구조

```
DjangoServer/
├── api/                          # Django API 엔드포인트
│   ├── views.py                  # API 뷰 함수
│   ├── urls.py                   # URL 라우팅
│   └── serializers.py            # 데이터 직렬화
├── RLmodels/                     # 강화학습 모델
│   ├── Agent/
│   │   └── A3CAgent.py          # A3C 에이전트 구현
│   ├── models/
│   │   └── A3CAgent_ActorCritic.py # Actor-Critic 네트워크
│   ├── env/
│   │   └── env.py               # 주식 거래 환경
│   ├── data/                    # 학습 데이터
│   └── output/                  # 학습된 모델 저장
├── modules/                      # 핵심 모듈
│   ├── Auth/                    # 인증 관리
│   ├── services/                # API 서비스
│   │   ├── buy_stock.py         # 매수 서비스
│   │   ├── sell_stock.py        # 매도 서비스
│   │   └── get_price.py         # 가격 조회
│   ├── config/                  # 설정 관리
│   └── utils/                   # 유틸리티
├── ChatGPT/                     # AI 챗봇
├── nginx/                       # Nginx 설정
└── docker-compose.yml           # Docker 설정
```

## 🚀 설치 및 실행

### 사전 요구사항

- **AWS EC2 인스턴스** (Amazon Linux 2, t3.large, 64GB)
- **Python 3.9+**
- **Docker & Docker Compose**
- **한국투자증권 API 키** (APP_KEY, APP_SECRET)
- **OpenAI API 키**
- **SSL 인증서** (HTTPS 사용)

### 1. 프로젝트 클론

```bash
git clone https://github.com/EazyNick/2024_RLTrading_A3C.git
cd 2024_RLTrading_A3C
```

### 2. 환경 설정

```bash
# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 3. API 키 설정

```bash
# 한국투자증권 API 키 설정
# DjangoServer/modules/Auth/Appkey.env
APP_KEY=your_app_key
APP_SECRET_KEY=your_secret_key

# OpenAI API 키 설정
# DjangoServer/ChatGPT/apikey.env
OPENAI_API_KEY=your_openai_api_key
```

### 4. Docker로 실행

```bash
# Docker 컨테이너 빌드 및 실행
docker-compose up -d --build
```

### 5. 서버 접속

- **웹 인터페이스**: `https://your-domain.com`
- **API 엔드포인트**: `https://your-domain.com/api/`

## 📊 모델 성능

### 학습 결과

- **학습 데이터**: KIA 주식 데이터 (2020-2024), 삼성 주식 데이터
- **테스트 기간**: 실제 거래 환경에서 테스트
- **초기 자본**: 10,000,000원
- **거래 수수료**: 0.015% (매수), 0.2% (매도 시 거래세)
- **최대 보유 주식**: 200주

### 모델 구조

```python
# Actor-Critic 네트워크
Input Layer (2) → Hidden Layer (256) → Policy Output (3) + Value Output (1)
```

## 🔧 API 문서

### 주요 엔드포인트

| 엔드포인트                         | 메소드 | 설명                                        |
| ---------------------------------- | ------ | ------------------------------------------- |
| `/api/stock_data/`                 | GET    | KOSPI/KOSDAQ 실시간 데이터 조회             |
| `/api/account/status/`             | GET    | 계좌 상태 조회 (account_id 파라미터 필요)   |
| `/api/stock_auto_trading_chatbot/` | POST   | AI 챗봇 상담 (message 파라미터)             |
| `/api/accounts/login/`             | POST   | 사용자 로그인 (Email, Password)             |
| `/api/accounts/register/`          | POST   | 사용자 회원가입 (Email, Password, username) |

### 데이터 형식

```json
{
  "stock_data": {
    "status": "success",
    "kospi_today": 2500.5,
    "kospi_latest": 2501.25,
    "kosdaq_today": 800.3,
    "kosdaq_latest": 801.15
  },
  "account_info": {
    "stock_info_list": [
      {
        "stock_code": "000270",
        "stock_name": "기아",
        "holding_quantity": 10,
        "purchase_price": 50000,
        "current_price": 55000,
        "profit_loss": 50000
      }
    ],
    "account_info": {
      "total_asset": 10000000,
      "cash_balance": 5000000,
      "stock_value": 5000000
    }
  },
  "chatbot_response": {
    "response": "AI 챗봇의 응답 메시지"
  }
}
```

## 🔒 보안 기능

- **API 키 암호화** 저장
- **HTTPS** 통신 암호화
- **CSRF 토큰** 인증
- **세션 관리** 및 자동 로그아웃
- **입력 데이터 검증** 및 sanitization

## 📈 성능 최적화

- **Celery 비동기 작업** 처리 (Redis 브로커)
- **스케줄링 최적화**:
  - 자동매매: 4시간마다 실행
  - 데이터 수집: 1시간마다 실행
  - KOSPI/KOSDAQ: 5분마다 실행
- **Docker 컨테이너화**로 리소스 효율성
- **Nginx 리버스 프록시**로 로드 분산
- **DynamoDB** NoSQL 데이터베이스 활용

## 🐛 문제 해결

### 일반적인 문제

1. **API 연결 오류**

   ```bash
   # API 키 확인
   cat DjangoServer/modules/Auth/Appkey.env
   ```

2. **모델 로딩 실패**

   ```bash
   # 모델 파일 경로 확인
   ls DjangoServer/RLmodels/output/
   ```

3. **Docker 실행 오류**

   ```bash
   # 컨테이너 로그 확인
   docker-compose logs
   ```

4. **Celery 작업 실패**

   ```bash
   # Celery 로그 확인
   docker-compose logs celery
   ```

5. **DynamoDB 연결 오류**

   ```bash
   # AWS 자격 증명 확인
   aws configure list
   ```

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 📞 문의

프로젝트에 대한 문의사항이나 제안사항이 있으시면 언제든지 연락주세요.

- **이메일**: kkkygsos@naver.com
- **GitHub**: [EazyNick](https://github.com/EazyNick)

## 🙏 감사의 말

- **한이음 ICT 멘토링** 프로그램 지원
- **한국과학기술원** 이규영 멘토님의 지도

---

**⚠️ 주의사항**: 이 시스템은 교육 및 연구 목적으로 개발되었습니다. 실제 투자에 사용할 경우 충분한 테스트와 리스크 관리가 필요합니다.
