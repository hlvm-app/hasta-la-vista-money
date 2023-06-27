from django.urls import path
from hasta_la_vista_money.expense.views import (
    ExpenseView,
    DeleteExpenseView,
    DeleteCategoryExpenseView,
)

app_name = 'expense'
urlpatterns = [
    path('', ExpenseView.as_view(), name='list'),
    path('<int:pk>/', DeleteExpenseView.as_view(), name='delete_expense'),
    path(
        'category/<int:pk>/',
        DeleteCategoryExpenseView.as_view(),
        name='delete_category_expense',
    ),
]
