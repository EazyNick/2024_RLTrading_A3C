"""
Django settings for DjangoServer project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

log_dir = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 슈퍼유저 자동 생성 설정
if 'DJANGO_SUPERUSER_USERNAME' in os.environ:
    # 슈퍼유저 설정
    DJANGO_SUPERUSER_USERNAME = os.environ['DJANGO_SUPERUSER_USERNAME']
    DJANGO_SUPERUSER_PASSWORD = os.environ['DJANGO_SUPERUSER_PASSWORD']
    DJANGO_SUPERUSER_EMAIL = os.environ['DJANGO_SUPERUSER_EMAIL']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7!i3ja1c_(g_0^gw+zs=)n!%bt%qx7^d*4j-)6bh_nuuv2x#y&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1',  '13.210.203.153', 'fintech19190301.kro.kr']

# Define the allowed methods
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# CSRF_TRUSTED_ORIGINS 설정
CORS_ALLOW_ALL_ORIGINS = True  # 개발 중에는 이렇게 설정하고, 프로덕션에서는 특정 도메인만 허용하도록 변경하세요.
# CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_HTTPONLY = False  # 모바일 앱에서 CSRF 쿠키를 사용할 수 있도록 설정

CSRF_TRUSTED_ORIGINS = [
    'https://fintech19190301.kro.kr',
]

# CORS_ALLOWED_ORIGINS = [
#     'https://fintech19190301.kro.kr',
# ]

# CSRF settings
CSRF_COOKIE_NAME = "csrftoken"
CSRF_HEADER_NAME = "HTTP_X_CSRFTOKEN"

#클라이언트에게 노출할 헤더
# CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
]

# CELERY_BEAT_SCHEDULE = {
#     'run-task-every-90000-seconds': {
#         'task': 'stock_app.tasks.run_task',
#         'schedule': 100.0,  # 60초마다 실행
#     },
# }

# Celery 설정
CELERY_BEAT_SCHEDULE = {
    'run-task-every-4-hours': {
        'task': 'stock_app.tasks.run_task',
        'schedule': 3600 * 4,  # 4시간마다 실행
    },
    'run-task2-every-1-hour': {
        'task': 'stock_app.tasks2.run_task2',
        'schedule': 3600,  # 1시간마다 실행
    },
    'run-task_saveKOSPIKOSDAQ-every-300-seconds': {
        'task': 'stock_app.tasks3.run_task_saveKOSPIKOSDAQ',
        'schedule': 300.0,  # 30초마다 실행
    },
}

CELERY_TASK_TIME_LIMIT = 300  # 5 minutes

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'api',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'stock_app',
    'django_extensions',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'DjangoServer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates/static'),  # Add this line
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': True,  # 디버그 모드 활성화
        },
    },
]


WSGI_APPLICATION = 'DjangoServer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_ROOT = os.path.join(BASE_DIR, 'static') # collectstatic 명령어로 모든 정적 파일을 모을 디렉토리를 지정
# BASE_DIR은 프로젝트의 기본 디렉토리 경로입니다.
# STATIC_ROOT는 모든 앱의 정적 파일을 모아 배포 준비를 할 디렉토리를 지정합니다.
# python manage.py collectstatic 명령어를 실행하면, 모든 정적 파일이 이 디렉토리에 복사됩니다.

# 보안 설정 (HTTPS)
# HTTP_X_FORWARDED_PROTO 헤더를 사용하여 클라이언트의 원래 프로토콜(http 또는 https)을 확인하고, Django가 이를 인식하여 HTTPS로 처리하도록 합니다.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 이 설정이 True로 설정되면, Django는 모든 HTTP 요청을 HTTPS로 자동 리디렉션합니다. 이를 통해 모든 통신이 암호화된 HTTPS를 통해 이루어지도록 보장
SECURE_SSL_REDIRECT = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'templates', 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'templates', 'media')

# Celery 로깅 설정
CELERY_WORKER_LOG_FILE = os.path.join(log_dir, "celery_worker.log")
CELERY_BEAT_LOG_FILE = os.path.join(log_dir, "celery_beat.log")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_dir, 'django_debug.log'),
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_dir, 'django_error.log'),
            'formatter': 'verbose',
        },
        'celery_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': CELERY_WORKER_LOG_FILE,
            'formatter': 'verbose',
        },
        'celery_beat_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': CELERY_BEAT_LOG_FILE,
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'error_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'mylogger': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'celery': {
            'handlers': ['celery_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'celery.beat': {
            'handlers': ['celery_beat_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}