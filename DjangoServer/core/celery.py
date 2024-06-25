from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django의 settings 모듈을 설정합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_monitor.settings')

app = Celery('market_monitor')

# Django 설정으로부터 configuration을 로드합니다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# 프로젝트의 모든 task 모듈을 로드합니다.
app.autodiscover_tasks()
