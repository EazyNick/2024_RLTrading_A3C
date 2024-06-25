# api/views.py

from django.shortcuts import render

from rest_framework import viewsets
from .models import MyModel
from .serializers import MyModelSerializer
from rest_framework.renderers import JSONRenderer

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    renderer_classes = [JSONRenderer]

import logging

logger = logging.getLogger('mylogger')

def home(request):
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
    return render(request, 'api/home.html')

    