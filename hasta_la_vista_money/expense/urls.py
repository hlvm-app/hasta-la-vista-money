from django.urls import path
from hasta_la_vista_money.expense.views import (
    ExpenseCategoryDeleteView,
    ExpenseCreateView,
    ExpenseDeleteView,
    ExpenseUpdateView,
    ExpenseView,
)

app_name = 'expense'
urlpatterns = [
    path('', ExpenseView.as_view(), name='list'),
    path('create/', ExpenseCreateView.as_view(), name='create'),
    path('change/<int:pk>/', ExpenseUpdateView.as_view(), name='change'),
    path('delete/<int:pk>/', ExpenseDeleteView.as_view(), name='delete'),
    path(
        'category/<int:pk>/',
        ExpenseCategoryDeleteView.as_view(),
        name='delete_category_expense',
    ),
]
