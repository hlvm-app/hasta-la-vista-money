from django.test import TestCase
from django.urls import reverse_lazy
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import HTTPStatus
from hasta_la_vista_money.expense.models import Expense, ExpenseType
from hasta_la_vista_money.users.models import User

TEST_AMOUNT = 15000


class TestExpense(TestCase):

    fixtures = [
        'users.yaml', 'account.yaml', 'expense.yaml', 'expense_cat.yaml',
    ]

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.account = Account.objects.get(pk=1)
        self.expense = Expense.objects.get(pk=1)
        self.expense_type = ExpenseType.objects.get(pk=1)

    def test_list_expense(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('expense:list'))
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)

    def test_expense_create(self):
        self.client.force_login(self.user)

        url = reverse_lazy('expense:list')

        new_expense = {
            'user': self.user,
            'account': self.account,
            'category': self.expense_type,
            'date': '20/12/2023 15:30',
            'amount': TEST_AMOUNT,
        }

        response = self.client.post(url, data=new_expense, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)

    def test_expense_delete(self):
        self.client.force_login(self.user)

        url = reverse_lazy('expense:delete_expense', args=(self.expense.pk, ))

        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)
