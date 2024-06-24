# api/views.py

from django.shortcuts import render

from rest_framework import viewsets
from .models import MyModel
from .serializers import MyModelSerializer

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer

import logging

logger = logging.getLogger('mylogger')



def home(request):
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
    return render(request, 'api/home.html')

    