from django.urls import path
from hasta_la_vista_money.expense.views import ExpenseView

app_name = 'expense'
urlpatterns = [
    path('', ExpenseView.as_view(), name='list'),
]
