from django.test import TestCase
from django.urls import reverse_lazy
from hasta_la_vista_money.loan.models import Loan
from hasta_la_vista_money.users.models import User


class TestLoan(TestCase):
    fixtures = [
        'users.yaml',
        'account.yaml',
        'income.yaml',
        'income_cat.yaml',
        'loan.yaml',
    ]

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.loan1 = Loan.objects.get(pk=2)
        self.loan2 = Loan.objects.get(pk=3)

    def test_list_loan(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('income:list'))
        self.assertEqual(response.status_code, 200)
