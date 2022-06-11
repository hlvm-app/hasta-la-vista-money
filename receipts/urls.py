from django.urls import path

from receipts.views import ReceiptView, AddReceiptView

app_name = 'receipts'
urlpatterns = [
    path('', ReceiptView.as_view(), name='list'),
    path('addreceipt', AddReceiptView.as_view(), name='add'),
    path('addreceipt/', AddReceiptView.as_view(), name='add_receipt'),
]
