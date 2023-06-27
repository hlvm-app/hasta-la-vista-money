from django.test import TestCase
from django.urls import reverse_lazy

from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import HTTPStatus
from hasta_la_vista_money.users.models import User


class TestAccount(TestCase):

    fixtures = ['users.yaml', 'account.yaml']

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.account1 = Account.objects.get(pk=1)
        self.account2 = Account.objects.get(pk=2)

    def test_account_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('applications:list'))
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)
        account_list = list(response.context['accounts'])
        self.assertQuerySetEqual(account_list, [self.account1, self.account2])

    def test_account_create(self):
        ...
