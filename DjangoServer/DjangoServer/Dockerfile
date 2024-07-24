# 베이스 이미지 설정 (빌드 단계)
FROM python:3.9 AS builder

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 종속성 파일 복사 및 설치
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# 프로젝트 파일 복사
COPY . /app/

# 최종 이미지를 위한 새로운 베이스 이미지 설정
FROM python:3.9-slim

# 필요한 런타임 라이브러리 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# # 스크립트 파일 복사
# COPY scripts/entrypoint.sh /scripts/entrypoint.sh
# RUN chmod +x /scripts/entrypoint.sh

# 환경 변수 설정
ENV DJANGO_SETTINGS_MODULE=DjangoServer.settings
# modules 디렉토리를 Python 경로에 추가
ENV PYTHONPATH="/app:${PYTHONPATH}"

# 포트 설정 (예: 8000)
EXPOSE 8000

CMD ["gunicorn", "DjangoServer.wsgi:application", "--bind", "0.0.0.0:8000"]
