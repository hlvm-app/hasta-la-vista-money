from django.urls import path
from hasta_la_vista_money.expense.views import (
    ChangeExpenseView,
    DeleteExpenseCategoryView,
    DeleteExpenseView,
    ExpenseView,
)

app_name = 'expense'
urlpatterns = [
    path('', ExpenseView.as_view(), name='list'),
    path('change/<int:pk>/', ChangeExpenseView.as_view(), name='change'),
    path('delete/<int:pk>/', DeleteExpenseView.as_view(), name='delete'),
    path(
        'category/<int:pk>/',
        DeleteExpenseCategoryView.as_view(),
        name='delete_category_expense',
    ),
]
