from django.urls import path

from users.views import CreateUser, ListUsers

app_name = 'users'
urlpatterns = [
    path('', ListUsers.as_view(), name='list'),
    path('registration/', CreateUser.as_view(), name='registration')
]
