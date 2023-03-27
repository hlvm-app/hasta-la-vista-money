import json
from os import environ

from bot.json_parse import ReceiptParser
from django.test import TestCase
from dotenv import load_dotenv

load_dotenv()

NUMBER_RECEIPT = 6888
TOTAL_SUM = 217.6
PRODUCT_LIST_LEN = 2
PRICE_PRODUCT1 = 131.32
PRICE_PRODUCT2 = 86.28
QUANTITY_PRODUCT1 = 1
QUANTITY_PRODUCT2 = 1
AMOUNT_PRODUCT1 = PRICE_PRODUCT1 * QUANTITY_PRODUCT1
AMOUNT_PRODUCT2 = PRICE_PRODUCT2 * QUANTITY_PRODUCT2


class ReceiptParserTestCase(TestCase):
    def setUp(self) -> None:
        with open('fixtures/receipt.json', 'r') as receipt_json:
            json_data = json.load(receipt_json)
        self.parser = ReceiptParser(json_data)
        self.parser.parse(environ.get('ID_GROUP_USER'))
        self.token = environ.get('TOKEN_TELEGRAM_BOT')

    def test_parse_receipt(self):
        self.assertIsNotNone(self.parser.receipt)
        self.assertEqual(self.parser.receipt.number_receipt, NUMBER_RECEIPT)
        self.assertEqual(self.parser.receipt.total_sum, TOTAL_SUM)
        self.assertEqual(len(self.parser.product_list), PRODUCT_LIST_LEN)

    def test_product_name(self):
        self.assertEqual(
            self.parser.product_list[0].product_name, 'Product One',
        )
        self.assertEqual(
            self.parser.product_list[1].product_name, 'Product Two',
        )

    def test_price(self):
        self.assertEqual(self.parser.product_list[0].price, PRICE_PRODUCT1)
        self.assertEqual(self.parser.product_list[1].price, PRICE_PRODUCT2)

    def test_quantity(self):
        self.assertEqual(
            self.parser.product_list[0].quantity, QUANTITY_PRODUCT1,
        )
        self.assertEqual(
            self.parser.product_list[1].quantity, QUANTITY_PRODUCT2,
        )

    def test_amount(self):
        self.assertEqual(self.parser.product_list[0].amount, AMOUNT_PRODUCT1)
        self.assertEqual(self.parser.product_list[1].amount, AMOUNT_PRODUCT2)
