from django.urls import path
from .views import SaveItemView, LoginView, AccountStatusView, get_csrf_token, StockAutoTradingChatbotView, StockDataView

urlpatterns = [
    path('accounts/', SaveItemView.as_view(), name='account-save'),
    path('accounts/login/', LoginView.as_view(), name='account-login'),  # 로그인 경로 추가
    path('account/status/', AccountStatusView.as_view(), name='account-status'),
    path('csrf/', get_csrf_token, name='get_csrf_token'),
    path('stock_auto_trading_chatbot/', StockAutoTradingChatbotView.as_view(), name='stock_auto_trading_chatbot'),
    path('stock_data/', StockDataView.as_view(), name='stock-data'), 
]
