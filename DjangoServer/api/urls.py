from django.urls import path
from .views import SaveItemView

urlpatterns = [
    path('items/', SaveItemView.as_view(), name='item-save'),
]
