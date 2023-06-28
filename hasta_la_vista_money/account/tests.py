from django.test import TestCase
from django.urls import reverse_lazy
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import HTTPStatus
from hasta_la_vista_money.users.models import User

BALANCE_TEST = 250000


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
        self.client.force_login(self.user)
        url = reverse_lazy('applications:list')

        new_account = {
            'name_account': 'Банковская карта *8090',
            'balance': BALANCE_TEST,
            'currency': 'RU',
        }

        response = self.client.post(url, data=new_account)
        self.assertRedirects(response, '/applications/')
        self.assertEqual(response.status_code, HTTPStatus.REDIRECTS.value)

        created_account = Account.objects.get(
            name_account='Банковская карта *8090',
        )
        self.assertEqual(created_account.balance, BALANCE_TEST)
        self.assertEqual(created_account.currency, 'RU')

    def test_account_delete(self):
        self.client.force_login(self.user)
        url = reverse_lazy(
            'applications:delete_account', args=(self.account2.pk, ),
        )
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, '/applications/')
