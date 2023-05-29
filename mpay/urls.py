from django.urls import path

from .views import get_access_token  # mpesaexpressquery,
from .views import mpesa_express, check_transaction_status, callback_view

urlpatterns = [
    path('', get_access_token, name='get_access_token'),
    path('mpesa-express/', mpesa_express, name='mpesa-express'),
    path('check-transaction-status/', check_transaction_status, name='check-transaction-status'),
    path('stkpush/callback/', callback_view, name='callback'),
]
