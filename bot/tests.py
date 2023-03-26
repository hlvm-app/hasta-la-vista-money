import json
from os import environ
from django.test import TestCase
from bot.json_parse import ReceiptParser

from dotenv import load_dotenv

load_dotenv()


class ReceiptParserTestCase(TestCase):

    def test_parse_receipt(self):
        with open('fixtures/receipt.json', 'r') as f:
            json_data = json.load(f)

        parser = ReceiptParser(json_data)

        parser.parse(environ.get('ID_GROUP_USER'))
        self.assertIsNotNone(parser.receipt)
        self.assertEqual(parser.receipt.number_receipt, 6887)
        self.assertEqual(parser.receipt.total_sum, 217.60)
        self.assertEqual(len(parser.product_list), 2)
        self.assertEqual(parser.product_list[0].product_name, 'Product One')
        self.assertEqual(parser.product_list[0].price, 131.32)
        self.assertEqual(parser.product_list[0].quantity, 1)
        self.assertEqual(parser.product_list[0].amount, 131.32)
        self.assertEqual(parser.product_list[1].product_name, 'Product Two')
        self.assertEqual(parser.product_list[1].price, 86.28)
        self.assertEqual(parser.product_list[1].quantity, 1)
        self.assertEqual(parser.product_list[1].amount, 86.28)
