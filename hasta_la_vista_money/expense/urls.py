from django.urls import path
from .views import ExpenseView

app_name = 'expense'
urlpatterns = [
    path('', ExpenseView.as_view(), name='list'),
]
