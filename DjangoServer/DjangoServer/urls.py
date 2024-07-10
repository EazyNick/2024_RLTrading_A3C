from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api import views 

router = routers.DefaultRouter()
router.register(r'items', views.ItemViewSet)  # 'items'로 등록

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # 'api/items/' 경로를 포함
]
