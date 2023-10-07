from django.test import TestCase
from django.urls import reverse_lazy
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import HTTPStatus
from hasta_la_vista_money.expense.models import Expense
from hasta_la_vista_money.income.models import Income
from hasta_la_vista_money.users.models import User

BALANCE_TEST = 250000
NEW_BALANCE_TEST = 450000


class TestAccount(TestCase):
    fixtures = [
        'users.yaml',
        'account.yaml',
        'expense.yaml',
        'expense_cat.yaml',
        'income.yaml',
        'income_cat.yaml',
    ]

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.account1 = Account.objects.get(pk=1)
        self.account2 = Account.objects.get(pk=2)
        self.expense = Expense.objects.get(pk=1)
        self.income = Income.objects.get(pk=1)

    def test_account_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('applications:list'))
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)
        account_list = list(response.context['accounts'])
        self.assertQuerySetEqual(account_list, [self.account1, self.account2])

    def test_account_create(self):
        self.client.force_login(self.user)
        url = reverse_lazy('account:create')

        new_account = {
            'user': self.user,
            'name_account': 'Банковская карта *8090',
            'balance': BALANCE_TEST,
            'currency': 'RU',
        }

        response = self.client.post(url, data=new_account, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)

        created_account = Account.objects.get(
            name_account='Банковская карта *8090',
        )
        self.assertEqual(created_account.balance, BALANCE_TEST)
        self.assertEqual(created_account.currency, 'RU')

    def test_update_account(self):
        self.client.force_login(self.user)
        url = reverse_lazy('account:change', args=(self.account1.pk,))
        update_account = {
            'user': self.user,
            'name_account': 'Основной счёт',
            'balance': NEW_BALANCE_TEST,
            'currency': 'RU',
        }
        response = self.client.post(url, update_account, follow=True)
        self.assertEqual(
            Account.objects.get(pk=self.account1.pk),
            self.account1,
        )
        self.assertRedirects(
            response,
            '/applications/',
            status_code=HTTPStatus.REDIRECTS.value,
        )

    def test_account_delete(self):
        self.client.force_login(self.user)
        url = reverse_lazy(
            'account:delete_account',
            args=(self.account2.pk,),
        )

        response = self.client.post(url, follow=True)
        self.assertRedirects(response, '/applications/')

    def test_delete_account_exist_expense(self):
        self.client.force_login(self.user)
        url1 = reverse_lazy('expense:list')

        url2 = reverse_lazy(
            'account:delete_account',
            args=(self.account1.pk,),
        )

        new_expense = {
            'user': self.user,
            'account': self.account1,
            'category': 'Банковский платёж',
            'date': '20/12/2023 15:30',
            'amount': '15000.00',
        }
        response = self.client.post(url1, data=new_expense)
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)

        expense_exists = Expense.objects.filter(account=self.account1).exists()
        self.assertTrue(expense_exists)

        response = self.client.post(url2, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)
        self.assertTrue(Account.objects.filter(pk=self.account1.pk).exists())
