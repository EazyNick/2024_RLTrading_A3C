# api/views.py

from django.shortcuts import render
from django.conf import settings
import os

import logging

logger = logging.getLogger('django')

def home_view(request):
    logger.debug('Home view has been accessed')
    return render(request, 'home.html')
    