from django.test import TestCase
from django.urls import reverse_lazy
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import HTTPStatus
from hasta_la_vista_money.receipts.models import Customer, Product, Receipt
from hasta_la_vista_money.users.models import User


class TestReceipt(TestCase):

    fixtures = [
        'users.yaml',
        'account.yaml',
        'receipt_receipt.yaml',
        'receipt_customer.yaml',
        'receipt_product.yaml',
    ]

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.account = Account.objects.get(pk=1)
        self.receipt = Receipt.objects.get(pk=1)
        self.customer = Customer.objects.get(pk=1)
        self.product = Product.objects.get(pk=1)

    def test_receipt_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('receipts:list'))
        self.assertEqual(response.status_code, HTTPStatus.SUCCESS_CODE.value)

    def test_receipt_create(self):
        self.client.force_login(self.user)
        url = reverse_lazy('receipts:create')

        new_product = {
            'user': self.user,
            'product_name': 'Яблоко',
            'price': 10,
            'quantity': 1,
            'amount': 10,
            'nds_type': 1,
            'nds_sum': 1.3,
        }

        new_receipt = {
            'user': self.user,
            'account': self.account,
            'receipt_date': '28/06/2023 21:24',
            'number_receipt': 111,
            'operation_type': 1,
            'total_sum': 10,
            'customer': 'ООО Рога и Копыта',
            'product': new_product,
        }

        response_product = self.client.post(url, data=new_product, follow=True)
        response_receipt = self.client.post(url, data=new_receipt, follow=True)

        self.assertEqual(
            response_product.status_code, HTTPStatus.SUCCESS_CODE.value,
        )
        self.assertEqual(
            response_receipt.status_code, HTTPStatus.SUCCESS_CODE.value,
        )

    def test_receipt_delete(self):
        self.client.force_login(self.user)
