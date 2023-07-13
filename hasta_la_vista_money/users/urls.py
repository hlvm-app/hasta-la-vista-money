from django.urls import path
from hasta_la_vista_money.users.views import (
    CreateUser,
    ListUsers,
    UpdateUserPasswordView,
    UpdateUserView,
)

app_name = 'users'
urlpatterns = [
    path('registration/', CreateUser.as_view(), name='registration'),
    path('profile/<int:pk>/', ListUsers.as_view(), name='profile'),
    path('update_user/<int:pk>', UpdateUserView.as_view(), name='update_user'),
    path(
        'change-password/<int:pk>/',
        UpdateUserPasswordView.as_view(),
        name='change_password',
    ),
]
