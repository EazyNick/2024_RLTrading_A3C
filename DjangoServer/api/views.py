from django.http import JsonResponse

def home(request):
    message = {
        'message': 'Hello, this is your response message!'
    }
    return JsonResponse(message)
