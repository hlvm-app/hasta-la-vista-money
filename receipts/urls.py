from django.urls import path

from receipts.views import receipt_view

app_name = 'receipts'
urlpatterns = [
    path('', receipt_view, name='list'),
]
