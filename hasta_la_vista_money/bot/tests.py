# import json
# from os import environ
#
# from django.test import TestCase
# from dotenv import load_dotenv
# from hasta_la_vista_money.bot.receipt_api_receiver import ReceiptParser
#
# load_dotenv()
#
# NUMBER_RECEIPT = 6888
# TOTAL_SUM = 217.6
# PRODUCT_LIST_LEN = 2
# PRICE_PRODUCT1 = 131.32
# PRICE_PRODUCT2 = 86.28
# QUANTITY_PRODUCT1 = 1
# QUANTITY_PRODUCT2 = 1
# AMOUNT_PRODUCT1 = PRICE_PRODUCT1 * QUANTITY_PRODUCT1
# AMOUNT_PRODUCT2 = PRICE_PRODUCT2 * QUANTITY_PRODUCT2
#
#
# class ReceiptParserTestCase(TestCase):
#
#     def setUp(self) -> None:
#         with open('fixtures/receipt.json', 'r') as receipt_json:
#             json_data = json.load(receipt_json)
#         self.parser = ReceiptParser(json_data)
#         self.parser.parse(int(environ.get('ID_GROUP_USER')))
#
#     def test_parse_receipt(self):  # noqa: WPS213
#         self.assertIsNotNone(self.parser.receipt)
#         self.assertEqual(self.parser.receipt.number_receipt, NUMBER_RECEIPT)
#         self.assertEqual(self.parser.receipt.total_sum, TOTAL_SUM)
#         self.assertEqual(len(self.parser.product_list), PRODUCT_LIST_LEN)
#         self.assertEqual(
#             self.parser.product_list[0].product_name, 'Product One',
#         )
#         self.assertEqual(
#             self.parser.product_list[1].product_name, 'Product Two',
#         )
#         self.assertEqual(self.parser.product_list[0].price, PRICE_PRODUCT1)
#         self.assertEqual(self.parser.product_list[1].price, PRICE_PRODUCT2)
#         self.assertEqual(
#             self.parser.product_list[0].quantity, QUANTITY_PRODUCT1,
#         )
#         self.assertEqual(
#             self.parser.product_list[1].quantity, QUANTITY_PRODUCT2,
#         )
#         self.assertEqual(self.parser.product_list[0].amount, AMOUNT_PRODUCT1)
#         self.assertEqual(self.parser.product_list[1].amount, AMOUNT_PRODUCT2)
