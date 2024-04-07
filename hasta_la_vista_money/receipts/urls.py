from django.urls import path
from hasta_la_vista_money.receipts.views import (
    CustomerCreateAPIView,
    CustomerCreateView,
    FileFieldFormView,
    ReceiptCreateAPIView,
    ReceiptCreateView,
    ReceiptDeleteView,
    ReceiptListAPIView,
    ReceiptView,
    SellerListAPIView,
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
        'upload/image',
        FileFieldFormView.as_view(),
        name='upload',
    ),
    path(
        'seller/<int:id>',
        SellerListAPIView.as_view(),
        name='seller',
    ),
]
