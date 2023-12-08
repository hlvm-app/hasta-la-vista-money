from django.urls import path
from hasta_la_vista_money.budget.views import (
    BudgetView,
    generate_date_list_view,
)

app_name = 'budget'
urlpatterns = [
    path('', BudgetView.as_view(), name='list'),
    path('generate-date/', generate_date_list_view, name='generate_date'),
]
