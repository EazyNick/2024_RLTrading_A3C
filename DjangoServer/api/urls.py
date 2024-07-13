from django.urls import path
from .views import SaveItemView, LoginView

urlpatterns = [
    path('accounts/', SaveItemView.as_view(), name='account-save'),
    path('accounts/login/', LoginView.as_view(), name='account-login'),  # 로그인 경로 추가
]
