from django.urls import path
from hasta_la_vista_money.income.views import (
    ChangeIncomeView,
    CreateIncomeView,
    DeleteIncomeCategoryView,
    DeleteIncomeView,
    IncomeView,
)

app_name = 'income'
urlpatterns = [
    path('', IncomeView.as_view(), name='list'),
    path('create/', CreateIncomeView.as_view(), name='create'),
    path('change/<int:pk>/', ChangeIncomeView.as_view(), name='change'),
    path('delete/<int:pk>/', DeleteIncomeView.as_view(), name='delete_income'),
    path(
        'category/<int:pk>/',
        DeleteIncomeCategoryView.as_view(),
        name='delete_category_income',
    ),
]
