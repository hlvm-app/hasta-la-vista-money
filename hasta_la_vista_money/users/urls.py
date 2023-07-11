from django.urls import path
from hasta_la_vista_money.users.views import (
    CreateUser,
    ListUsers,
    UpdateUserPasswordView,
    UpdateUserView,
)

app_name = 'users'
urlpatterns = [
    path('', ListUsers.as_view(), name='list'),
    path('registration/', CreateUser.as_view(), name='registration'),
    path('update_user/<int:pk>', UpdateUserView.as_view(), name='update_user'),
    path(
        'change-password/<int:pk>/',
        UpdateUserPasswordView.as_view(),
        name='change_password',
    ),
]
