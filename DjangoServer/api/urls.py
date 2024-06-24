from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyModelViewSet

router = DefaultRouter()
router.register(r'mymodel', MyModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    path('home/', views.home, name='home'),  # 'home' 뷰를 'home/' 경로에 매핑
]
