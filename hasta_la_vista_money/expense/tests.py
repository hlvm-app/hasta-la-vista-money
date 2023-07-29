from django.test import TestCase
from django.urls import reverse_lazy
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import HTTPStatus
from hasta_la_vista_money.expense.forms import AddExpenseForm
from hasta_la_vista_money.expense.models import Expense, ExpenseType
from hasta_la_vista_money.users.models import User

TEST_AMOUNT = 15000
NEW_TEST_AMOUNT = 25000


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
            'date': '2023/12/20 15:30:00',
            'amount': TEST_AMOUNT,
        }

        response = self.client.post(url, data=new_expense, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)

    def test_expense_update(self):
        self.client.force_login(user=self.user)
        url = reverse_lazy('expense:change', kwargs={'pk': self.expense.id})
        update_expense = {
            'account': self.account.id,
            'category': self.expense_type.id,
            'date': '2023-06-30 22:31:54',
            'amount': NEW_TEST_AMOUNT,
        }

        form = AddExpenseForm(data=update_expense)
        self.assertTrue(form.is_valid())

        response = self.client.post(url, form.data)
        self.assertEqual(response.status_code, HTTPStatus.REDIRECTS.value)

        updated_expense = Expense.objects.get(pk=self.expense.id)
        self.assertEqual(updated_expense.amount, NEW_TEST_AMOUNT)

    def test_expense_delete(self):
        self.client.force_login(self.user)

        url = reverse_lazy('expense:delete', args=(self.expense.pk, ))

        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)
