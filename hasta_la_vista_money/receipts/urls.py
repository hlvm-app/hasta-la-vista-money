from django.urls import path
from hasta_la_vista_money.receipts.views import (
    CustomerCreateView,
    ReceiptCreateView,
    ReceiptDeleteView,
    ReceiptListCreateAPIView,
    ReceiptView,
)

app_name = 'receipts'
urlpatterns = [
    path('', ReceiptView.as_view(), name='list'),
    path('create/', ReceiptCreateView.as_view(), name='create'),
    path(
        'create_customer/',
        CustomerCreateView.as_view(),
        name='create_customer',
    ),
    path('<int:pk>/', ReceiptDeleteView.as_view(), name='delete'),
    path(
        'api/create',
        ReceiptListCreateAPIView.as_view(),
        name='api_list',
    ),
]
