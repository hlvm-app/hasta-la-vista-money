from django.test import Client, TestCase
from django.urls import reverse_lazy
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import HTTPStatus
from hasta_la_vista_money.expense.models import Expense, ExpenseType
from hasta_la_vista_money.users.models import User

TEST_AMOUNT = 15000
NEW_TEST_AMOUNT = 25000


class TestExpense(TestCase):

    fixtures = [
        'users.yaml', 'account.yaml', 'expense.yaml', 'expense_cat.yaml',
    ]

    def setUp(self) -> None:
        self.client = Client()
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

    def test_expense_update(self):
        self.client.force_login(user=self.user)
        url = reverse_lazy('expense:change', kwargs={'pk': self.expense.id})

        update_expense = {
            'user': self.user,
            'account': self.account,
            'category': self.expense_type,
            'date': '30/06/2023 22:31:54',
            'amount': NEW_TEST_AMOUNT,
        }

        response = self.client.post(url, update_expense)
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)

    def test_expense_delete(self):
        self.client.force_login(self.user)

        url = reverse_lazy('expense:delete', args=(self.expense.pk, ))

        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)
