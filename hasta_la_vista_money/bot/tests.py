import json
from os import environ

from django.test import TestCase
from dotenv import load_dotenv
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.bot.receipt_parse import ReceiptParser
from hasta_la_vista_money.users.models import User

load_dotenv()

NUMBER_RECEIPT = 708
TOTAL_SUM = 6.99
PRODUCT_LIST_LEN = 1
PRICE_PRODUCT1 = 6.99
QUANTITY_PRODUCT1 = 1
AMOUNT_PRODUCT1 = PRICE_PRODUCT1 * QUANTITY_PRODUCT1


class ReceiptParserTestCase(TestCase):
    fixtures = ['users.yaml', 'account.yaml']

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.account = Account.objects.get(pk=1)
        with open('fixtures/receipt.json', 'r') as receipt_json:
            json_data = json.load(receipt_json)
        self.parser = ReceiptParser(json_data, self.user, self.account.id)
        self.parser.parse_receipt(int(environ.get('ID_GROUP_USER')))

    def test_parse_receipt(self):
        self.assertIsNotNone(self.parser.receipt)
        self.assertEqual(self.parser.receipt.number_receipt, NUMBER_RECEIPT)
        self.assertEqual(self.parser.receipt.total_sum, TOTAL_SUM)
        self.assertEqual(len(self.parser.product_list), PRODUCT_LIST_LEN)
        self.assertEqual(
            self.parser.product_list[0].product_name,
            'Пакет ЛЕНТА майка 9кг',
        )
        self.assertEqual(self.parser.product_list[0].price, PRICE_PRODUCT1)
        self.assertEqual(
            self.parser.product_list[0].quantity,
            QUANTITY_PRODUCT1,
        )
        self.assertEqual(self.parser.product_list[0].amount, AMOUNT_PRODUCT1)
