from django.urls import path
from hasta_la_vista_money.income.views import (
    IncomeCategoryDeleteView,
    IncomeDeleteView,
    IncomeView,
)

app_name = 'income'
urlpatterns = [
    path('', IncomeView.as_view(), name='list'),
    path('<int:pk>/', IncomeDeleteView.as_view(), name='income_delete'),
    path(
        'category/<int:pk>/',
        IncomeCategoryDeleteView.as_view(),
        name='income_category_delete',
    ),
]
