from __future__ import absolute_import, unicode_literals

# Celery 앱을 항상 임포트하여 Django가 시작될 때 이를 사용할 수 있도록 합니다.
from DjangoServer.core.celery import app as celery_app

__all__ = ('celery_app',)
