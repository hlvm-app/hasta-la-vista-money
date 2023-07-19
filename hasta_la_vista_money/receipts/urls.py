from django.urls import path
from hasta_la_vista_money.receipts.views import (
    CreateReceiptView,
    ReceiptDeleteView,
    ReceiptView,
)

app_name = 'receipts'
urlpatterns = [
    path('', ReceiptView.as_view(), name='list'),
    path('create/', CreateReceiptView.as_view(), name='create'),
    path('<int:pk>/', ReceiptDeleteView.as_view(), name='delete'),
]
