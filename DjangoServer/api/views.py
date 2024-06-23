# api/views.py
from django.http import JsonResponse
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, world!")

# def home(request):
#     data = {
#         'message': 'Welcome to the home API!',
#         'status': 'success'
#     }
#     return JsonResponse(data)
