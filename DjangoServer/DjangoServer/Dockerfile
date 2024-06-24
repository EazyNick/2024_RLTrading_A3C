FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 파일 복사 및 설치
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# 프로젝트 파일 복사
COPY . /app/

# 환경 변수 설정
ENV DJANGO_SETTINGS_MODULE=DjangoServer.settings

# 포트 설정 (예: 8000)
EXPOSE 8000

# 서버 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "DjangoServer.wsgi:application"]
