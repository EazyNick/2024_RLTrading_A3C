# api/views.py

from django.shortcuts import render
from django.conf import settings
import os

import logging

logger = logging.getLogger('mylogger')

def home(request):
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
    return render(request, 'api/home.html')

    