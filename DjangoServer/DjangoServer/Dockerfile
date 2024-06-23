FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
COPY DjangoServer/requirements.txt /app/
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 복사
COPY . /app/

# uWSGI 설정 파일 복사
COPY DjangoServer/uwsgi.ini /app/DjangoServer/uwsgi.ini   

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=DjangoServer.settings

# uWSGI 실행
CMD ["uwsgi", "--ini", "/app/DjangoServer/uwsgi.ini"]
