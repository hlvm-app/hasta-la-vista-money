from django.urls import path
from hasta_la_vista_money.loan.views import LoanView

app_name = 'loan'
urlpatterns = [
    path('', LoanView.as_view(), name='list'),
]
