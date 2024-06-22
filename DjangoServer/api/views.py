# api/views.py
from django.http import JsonResponse

def home(request):
    data = {
        'message': 'Welcome to the home API!',
        'status': 'success'
    }
    return JsonResponse(data)
