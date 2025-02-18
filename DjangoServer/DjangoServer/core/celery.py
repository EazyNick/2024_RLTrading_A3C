from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Django 기본 설정 모듈
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoServer.settings')

app = Celery('DjangoServer')

# Django 설정에서 설정 불러오기
app.config_from_object('django.conf:settings', namespace='CELERY')

# # Django 프로젝트의 모든 task 모듈을 로드합니다.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# app.autodiscover_tasks() 

# Django 프로젝트의 모든 task 모듈을 수동으로 로드합니다.
# app.autodiscover_tasks(['stock_app'])

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
