import types

from bot.config_bot import bot_admin
from bot.services import convert_date_time, convert_price
from hasta_la_vista_money.receipts.models import Customer, Product, Receipt

CONSTANT_RECEIPT = types.MappingProxyType(
    {
        'name_seller': 'user',
        'retail_place_address': 'retailPlaceAddress',
        'retail_place': 'retailPlace',
        'receipt_date': 'dateTime',
        'operation_type': 'operationType',
        'total_sum': 'totalSum',
        'product_name': 'name',
        'price': 'price',
        'quantity': 'quantity',
        'amount': 'sum',
        'nds_type': 'nds',
        'nds_sum': 'ndsSum',
        'items': 'items',
    },
)


class JsonParser:
    def __init__(self, json_data):
        self.json_data = json_data

    def parse_json(self, json_data: dict, key: str):
        return JsonParser.get_value(self, json_data, key)

    def get_value(self, dictionary, key):
        if not isinstance(dictionary, dict):
            return None

        dict_value = dictionary.get(key)
        if dict_value is not None:
            return dict_value

        for nested_dict in dictionary.values():
            dict_value = self.get_value(nested_dict, key)
            if dict_value is not None:
                return dict_value

        return None


class ReceiptParser:
    def __init__(self, json_data, chat_id):
        self.json_data = json_data
        self.parser = JsonParser(self.json_data)
        self.customer = None
        self.receipt = None
        self.product_list = []

    def parse_customer(self):
        name_seller = self.parser.parse_json(
            self.json_data, CONSTANT_RECEIPT.get('name_seller'),
        )
        retail_place_address = self.parser.parse_json(
            self.json_data, CONSTANT_RECEIPT.get('retailPlaceAddress', None),
        )
        retail_place = self.parser.parse_json(
            self.json_data, CONSTANT_RECEIPT.get('retailPlace', None),
        )
        self.customer = Customer.objects.create(
            name_seller=name_seller,
            retail_place_address=retail_place_address,
            retail_place=retail_place,
        )

    def parse_receipt(self):
        receipt_date = convert_date_time(self.parser.parse_json(
            self.json_data, CONSTANT_RECEIPT.get('receipt_date'),
        ))
        operation_type = self.parser.parse_json(
            self.json_data, CONSTANT_RECEIPT.get('operation_type'),
        )
        total_sum = convert_price(self.parser.parse_json(
            self.json_data, CONSTANT_RECEIPT.get('total_sum'),
        ))
        customer = self.customer
        self.receipt = Receipt.objects.create(
            receipt_date=receipt_date,
            operation_type=operation_type,
            total_sum=total_sum,
            customer=customer,
        )

    def parse_products(self):  # noqa: WPS210
        products_list = self.parser.parse_json(
            self.json_data, CONSTANT_RECEIPT.get('items'),
        )
        for product in products_list:
            product_name = self.parser.parse_json(
                product, CONSTANT_RECEIPT.get('product_name'),
            )
            price = convert_price(
                self.parser.parse_json(
                    product, CONSTANT_RECEIPT.get('price'),
                ),
            )
            quantity = self.parser.parse_json(
                product, CONSTANT_RECEIPT.get('quantity'),
            )
            amount = convert_price(self.parser.parse_json(
                product, CONSTANT_RECEIPT.get('amount'),
            ))
            nds_type = self.parser.parse_json(
                product, CONSTANT_RECEIPT.get('nds_type', None),
            )
            nds_sum = convert_price(self.parser.parse_json(
                product, CONSTANT_RECEIPT.get('nds_sum', None),
            ))
            products = Product.objects.create(
                product_name=product_name,
                price=price,
                quantity=quantity,
                amount=amount,
                nds_type=nds_type,
                nds_sum=nds_sum,
            )
            self.product_list.append(products)
        self.receipt.product.set(self.product_list)

    def parse(self, chat_id):
        self.parse_customer()
        self.parse_receipt()
        self.parse_products()
        bot_admin.send_message(chat_id, 'Чек принят!')