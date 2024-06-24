from django.shortcuts import render

def home(request):
    context = {
        'name': 'Your Name'
    }
    return render(request, 'home.html', context)
