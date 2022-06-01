from django.test import TestCase
from django.urls import reverse_lazy

from receipts.models import Receipt
from users.models import User


class TestReceipt(TestCase):

    fixtures = ['receipts.yaml', 'users.yaml']

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.receipt1 = Receipt.objects.get(pk=4)
        self.receipt2 = Receipt.objects.get(pk=5)

    def test_receipt_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('receipts:list'))
        self.assertEqual(response.status_code, 200)
        receipts_list = list(response.context['receipts'])
        self.assertQuerysetEqual(receipts_list, [self.receipt1, self.receipt2])
