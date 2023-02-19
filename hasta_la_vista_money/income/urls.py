from django.urls import path

from hasta_la_vista_money.income.views import IncomeView, AddIncome

app_name = 'income'
urlpatterns = [
    path('', IncomeView.as_view(), name='list'),
    path('create/', AddIncome.as_view(), name='create')
]
