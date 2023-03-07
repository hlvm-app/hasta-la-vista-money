from django.urls import path
from hasta_la_vista_money.receipts.views import ReceiptCreateView, ReceiptView

app_name = 'receipts'
urlpatterns = [
    path('', ReceiptView.as_view(), name='list'),
    path('create/', ReceiptCreateView.as_view(), name='create'),
]
