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
    path('<int:pk>/', ChangeExpenseView.as_view(), name='change'),
    path('<int:pk>/', DeleteExpenseView.as_view(), name='delete_expense'),
    path(
        'category/<int:pk>/',
        DeleteExpenseCategoryView.as_view(),
        name='delete_category_expense',
    ),
]
