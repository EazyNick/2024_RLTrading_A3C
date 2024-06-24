#!/bin/bash

# 데이터베이스 마이그레이션
python manage.py migrate

# 슈퍼유저 생성 (환경 변수 사용)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
    python manage.py createsuperuser --no-input || true
fi

# Gunicorn 서버 실행
exec gunicorn --bind 0.0.0.0:8000 DjangoServer.wsgi:application
