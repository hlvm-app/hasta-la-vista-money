from django.urls import path
from hasta_la_vista_money.receipts.apis import (
    CustomerCreateAPIView,
    ReceiptCreateAPIView,
    ReceiptListAPIView,
    SellerListAPIView,
)
from hasta_la_vista_money.receipts.views import (
    CustomerCreateView,
    ReceiptCreateView,
    ReceiptDeleteView,
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
        'api/list',
        ReceiptListAPIView.as_view(),
        name='api_list',
    ),
    path(
        'api/create',
        ReceiptCreateAPIView.as_view(),
        name='receipt_api_create',
    ),
    path(
        'customer/api/create',
        CustomerCreateAPIView.as_view(),
        name='api_list',
    ),
    path(
        'seller/<int:id>',
        SellerListAPIView.as_view(),
        name='seller',
    ),
]
