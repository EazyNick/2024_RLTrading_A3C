from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),  # 'home' 뷰를 'home/' 경로에 매핑
]
