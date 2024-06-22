FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# 로그 디렉토리 생성
RUN mkdir -p /app/logs

COPY uwsgi.ini /app/

CMD ["uwsgi", "--ini", "uwsgi.ini"]