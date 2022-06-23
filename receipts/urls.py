from django.urls import path

from receipts.views import ReceiptView

app_name = 'receipts'
urlpatterns = [
    path('', ReceiptView.as_view(), name='list'),
]
