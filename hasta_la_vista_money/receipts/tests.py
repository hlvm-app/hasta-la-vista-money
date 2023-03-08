from django.test import TestCase
from django.urls import reverse_lazy
from hasta_la_vista_money.receipts.models import Customer, Product, Receipt
from hasta_la_vista_money.users.models import User


class TestReceipt(TestCase):

    fixtures = ['receipt.yaml', 'users.yaml', 'customer.yaml', 'product.yaml']
    status_code_ok = 200

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.receipt = Receipt.objects.get(pk=1)
        self.customer = Customer.objects.get(pk=1)
        self.product1 = Product.objects.get(pk=1)
        self.product2 = Product.objects.get(pk=2)

    def test_receipt_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('receipts:list'))
        self.assertEqual(response.status_code, self.status_code_ok)

    def test_product(self):
        self.client.force_login(self.user)
        self.assertEqual(self.receipt.product.count(), 2)
        self.assertIn(self.product1, self.receipt.product.all())
        self.assertIn(self.product2, self.receipt.product.all())

    def test_customer_create(self):
        self.client.force_login(self.user)
        self.customer = Customer.objects.create(
            name_seller='ООО "Пятерочка"',
            retail_place_address='Test Address',
            retail_place='Test place',
        )
        self.assertEqual(self.customer.pk, 2)

    def test_delete_customer(self):
        customer = Customer.objects.get(pk=1)
        customer.delete()
        with self.assertRaises(Customer.DoesNotExist):
            Customer.objects.get(pk=1)
