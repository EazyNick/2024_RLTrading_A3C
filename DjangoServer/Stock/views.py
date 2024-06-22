from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})

import logging
from django.http import HttpResponse, HttpResponseNotFound

logger = logging.getLogger('django')

def my_view(request):
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    return HttpResponse("Logging test")

def custom_404_view(request, exception):
    logger.error(f"404 error at {request.path}")
    return HttpResponseNotFound("404 Not Found")
