from django.contrib import admin
from .models import Item  # Item 모델을 가져옵니다.

admin.site.register(Item)  # Item 모델을 admin 사이트에 등록합니다.
