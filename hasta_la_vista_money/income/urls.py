from django.urls import path

from hasta_la_vista_money.income.views import IncomeView

app_name = 'income'
urlpatterns = [
    path('', IncomeView.as_view(), name='list'),
]
