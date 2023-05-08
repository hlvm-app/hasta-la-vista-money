from django.urls import path
from hasta_la_vista_money.bot.webhooks import webhooks

app_name = 'bot'

urlpatterns = [
    path('webhooks/', webhooks, name='webhooks'),
]
