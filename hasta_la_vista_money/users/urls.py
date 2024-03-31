from django.urls import path
from hasta_la_vista_money.users.views import (
    CreateUser,
    CustomPasswordResetConfirmView,
    ForgotPasswordView,
    ListUsers,
    ListUsersAPIView,
    LoginUserAPIView,
    UpdateUserPasswordView,
    UpdateUserView,
)

app_name = 'users'
urlpatterns = [
    path('registration/', CreateUser.as_view(), name='registration'),
    path('profile/<int:pk>/', ListUsers.as_view(), name='profile'),
    path('login/', LoginUserAPIView.as_view(), name='login'),
    path('update_user/<int:pk>', UpdateUserView.as_view(), name='update_user'),
    path(
        'change-password/<int:pk>/',
        UpdateUserPasswordView.as_view(),
        name='change_password',
    ),
    path(
        'forgot-password/',
        ForgotPasswordView.as_view(),
        name='forgot-password',
    ),
    path(
        'reset-password/<str:uidb64>/<str:token>/',
        CustomPasswordResetConfirmView.as_view(),
        name='custom-password-reset-confirm',
    ),
    path(
        'list/user',
        ListUsersAPIView.as_view(),
        name='list_user',
    ),
]
