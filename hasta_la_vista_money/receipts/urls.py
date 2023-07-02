from django.urls import path
from hasta_la_vista_money.receipts.views import ReceiptView, ReceiptDeleteView

app_name = 'receipts'
urlpatterns = [
    path('', ReceiptView.as_view(), name='list'),
    path('<int:pk>/', ReceiptDeleteView.as_view(), name='delete'),
]
