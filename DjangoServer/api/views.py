from django.http import JsonResponse

def home_view(request):
    data = {
        'key': 'value',  # 여기에 Flutter 애플리케이션으로 보낼 데이터를 넣습니다.
    }
    return JsonResponse(data)
