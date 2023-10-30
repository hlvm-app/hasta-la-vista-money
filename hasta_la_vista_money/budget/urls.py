from django.urls import path
from hasta_la_vista_money.budget.views import BudgetView

app_name = 'budget'
urlpatterns = [
    path('', BudgetView.as_view(), name='list'),
]
