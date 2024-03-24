from django.urls import path
from hasta_la_vista_money.account.views import (
    AccountCreateView,
    AccountListCreateAPIView,
    AccountView,
    ChangeAccountView,
    DeleteAccountView,
    TransferMoneyAccountView,
)

app_name = 'account'
urlpatterns = [
    path('', AccountView.as_view(), name='list'),
    path('create/', AccountCreateView.as_view(), name='create'),
    path('change/<int:pk>/', ChangeAccountView.as_view(), name='change'),
    path(
        'delete/<int:pk>',
        DeleteAccountView.as_view(),
        name='delete_account',
    ),
    path(
        'transfer-money/',
        TransferMoneyAccountView.as_view(),
        name='transfer_money',
    ),
    path(
        'api/list',
        AccountListCreateAPIView.as_view(),
        name='api_list',
    ),
]
