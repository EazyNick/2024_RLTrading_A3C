# 2024_RLTrading_Source

## 개요
`2024_RLTrading_Source`는 강화학습 모델을 활용한 주식 자동매매 시스템입니다. 이 시스템은 Django, Nginx, AWS EC2 (Amazon Linux 2) 환경에서 동작하며, 한국투자증권 REST API를 이용하여 현재가 조회, 계좌 조회, 매수, 매도를 자동으로 수행합니다.

## 기능
- **강화학습 모델(A3C)**: 주식 자동매매를 위한 강화학습 모델 구현
- **Django 서버**: 웹 인터페이스 및 백엔드 로직 처리
- **Nginx**: 웹 서버 및 리버스 프록시 설정
- **AWS EC2**: Amazon Linux 2 환경에서 서버 배포
- **한국투자증권 REST API**:
  - 현재가 조회
  - 계좌 조회
  - 매수 및 매도 자동화

## 설치 및 설정

### 사전 요구 사항
- AWS EC2 인스턴스 (Amazon Linux 2), Instance type - t3.large and Volume size (GiB) - 64GB
- Python 3.9 이상 버전
- Django 4.2.13
- Nginx
- Gunicorn
- Git
- 한국투자증권 REST API 사용을 위한 API Key, API SECRET KEY
- https 사용을 위한 도메인 및 ssl 인증서
- CHAT GPT API 키

### 1. AWS EC2 인스턴스 설정
1. AWS 콘솔에서 EC2 인스턴스를 생성하고 Amazon Linux 2 AMI를 선택합니다.
2. 인스턴스 생성 후, 보안 그룹에서 80 (HTTP) 및 22 (SSH) 포트를 열어줍니다.
3. SSH를 통해 EC2 인스턴스에 접속합니다.

### 2. 프로젝트 클론 및 환경 설정
1. Python 및 필요한 패키지를 설치합니다.
    ```bash
    sudo yum update -y
    sudo yum install -y python3 git
    sudo pip3 install virtualenv
    ```

2. 프로젝트를 클론하고 가상 환경을 설정합니다.
    ```bash
    git clone https://github.com/EazyNick/2024_RLTrading_A3C.git
    cd 2024_RLTrading_A3C
    virtualenv venv
    source venv/bin/activate
    ```

3. 프로젝트 의존성을 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```

4. Django 설정 파일을 수정하여 데이터베이스 및 기타 설정을 업데이트합니다.
    ```bash
    # 한국투자증권 API 키 설정
    # DjangoServer\modules\Auth\Appkey.env
    APP_KEY=your_app_key
    APP_SECRET_KEY=your_secret_key

    # CHAT GPT API 키 설정
    # DjangoServer\ChatGPT\apikey.env
    OPENAI_API_KEY=your_api_key
    ```

### 3. Nginx 설정
1. Nginx를 설치하고 설정 파일을 수정합니다.
2. Nginx 설정 파일 (`DjangoServer\nginx\nginx.conf`)을 수정하여 Django 애플리케이션과 연결합니다.

## 사용 방법
1. docker-compose.yml 파일이 있는 디렉토리에서, docker-compose up -d --build 명령어를 통해 빌드합니다.
2. 백그라운드에서 강화학습 모델을 통해 자동매매가 실행됩니다.
3. 웹 브라우저를 통해 서버에 접속합니다 (예: `http://your_server_domain_or_IP`).
4. 웹 인터페이스를 통해 계좌 조회 기능을 사용할 수 있습니다.

## 기여 방법
1. 이 프로젝트를 포크합니다.
2. 새로운 브랜치를 생성합니다 (`git checkout -b feature/YourFeature`).
3. 변경 사항을 커밋합니다 (`git commit -m 'Add some feature'`).
4. 브랜치에 푸시합니다 (`git push origin feature/YourFeature`).
5. 풀 리퀘스트를 생성합니다.

## 라이센스
이 프로젝트는 MIT 라이센스를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.
