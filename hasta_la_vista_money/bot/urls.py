from django.urls import path
from .views import webhooks


app_name = 'bot'

urlpatterns = [
    path('webhooks/', webhooks, name='webhooks')
]
