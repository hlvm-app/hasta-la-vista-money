from django.test import Client, TestCase
from django.urls import reverse_lazy
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import HTTPStatus
from hasta_la_vista_money.income.models import Income, IncomeType
from hasta_la_vista_money.users.models import User

TEST_AMOUNT = 15000
NEW_TEST_AMOUNT = 25000


class TestIncome(TestCase):

    fixtures = [
        'users.yaml', 'account.yaml', 'income.yaml', 'income_cat.yaml',
    ]

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.account = Account.objects.get(pk=1)
        self.income = Income.objects.get(pk=1)
        self.income_type = IncomeType.objects.get(pk=1)

    def test_list_income(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('income:list'))
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)

    def test_income_create(self):
        self.client.force_login(self.user)

        url = reverse_lazy('income:list')

        new_income = {
            'user': self.user,
            'account': self.account,
            'category': self.income_type,
            'date': '20/12/2023 15:30',
            'amount': TEST_AMOUNT,
        }

        response = self.client.post(url, data=new_income, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)

    def test_income_update(self):
        self.client.force_login(self.user)
        url = reverse_lazy('income:change', args=(self.income.pk,))
        update_expense = {
            'user': self.user,
            'category': self.income_type,
            'account': self.account,
            'date': '15/02/2023 15:30',
            'amount': NEW_TEST_AMOUNT,
        }

        response = self.client.post(url, update_expense)

        self.assertEqual(
            Income.objects.get(pk=self.income.pk), self.income,
        )
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)

    def test_income_delete(self):
        self.client.force_login(self.user)

        url = reverse_lazy('income:delete_income', args=(self.income.pk, ))

        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)
