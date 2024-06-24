# api/views.py

from django.shortcuts import render
from django.conf import settings
import os

def home(request):
    context = {
        'name': 'Your Name',
        'template_dirs': settings.TEMPLATES[0]['DIRS'],
        'template_app_dirs': settings.TEMPLATES[0]['APP_DIRS'],
        'template_path': os.path.join(settings.BASE_DIR, 'api/templates/api/home.html')
    }
    return render(request, 'api/home.html', context)
