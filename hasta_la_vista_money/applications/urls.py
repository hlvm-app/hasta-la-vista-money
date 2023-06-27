from django.urls import path
from hasta_la_vista_money.applications.views import (
    DeleteAccountView,
    PageApplication,
)

app_name = 'applications'
urlpatterns = [
    path('', PageApplication.as_view(), name='list'),
    path(
        'account/<int:pk>',
        DeleteAccountView.as_view(),
        name='delete_account'
    ),
]
