from django.urls import path
from hasta_la_vista_money.loan.views import (
    LoanCreateView,
    LoanView,
    PaymentMakeView,
)

app_name = 'loan'
urlpatterns = [
    path('', LoanView.as_view(), name='list'),
    path('create/', LoanCreateView.as_view(), name='create'),
    path('payment/create/', PaymentMakeView.as_view(), name='payment_create'),
]
