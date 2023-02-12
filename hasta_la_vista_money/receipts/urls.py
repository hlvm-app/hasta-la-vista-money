from django.urls import path

from hasta_la_vista_money.receipts.views import ReceiptView, CreateReceipt

app_name = 'receipts'
urlpatterns = [
    path('', ReceiptView.as_view(), name='list'),
    path('create/', CreateReceipt.as_view(), name='create')
]
