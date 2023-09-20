from django.urls import path
from hasta_la_vista_money.applications.views import (
    ChangeAccountView,
    DeleteAccountView,
    TransferMoneyAccountView,
)

app_name = 'account'
urlpatterns = [
    path(
        '<int:pk>',
        DeleteAccountView.as_view(),
        name='delete_account',
    ),
    path(
        'change/<int:pk>/',
        ChangeAccountView.as_view(),
        name='change',
    ),
    path(
        'transfer-money/',
        TransferMoneyAccountView.as_view(),
        name='transfer_money',
    ),
]
