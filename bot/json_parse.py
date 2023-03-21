import types

from bot.config_bot import bot_admin
from bot.services import ParseJson, convert_date_time, convert_price
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


def parse_receipt(json_data, chat_id):  # noqa: WPS210
    parser = ParseJson(json_data)

    # Getting of receipt items without products
    name_seller = parser.parse_json(
        json_data, CONSTANT_RECEIPT.get('name_seller'),
    )
    retail_place_address = parser.parse_json(
        json_data, CONSTANT_RECEIPT.get('retail_place_address'),
    )
    retail_place = parser.parse_json(
        json_data, CONSTANT_RECEIPT.get('retail_place'),
    )
    customer = Customer.objects.create(
        name_seller=name_seller,
        retail_place_address=retail_place_address,
        retail_place=retail_place,
    )

    receipt_date = convert_date_time(parser.parse_json(
        json_data, CONSTANT_RECEIPT.get('receipt_date'),
    ))
    operation_type = parser.parse_json(
        json_data, CONSTANT_RECEIPT.get('operation_type'),
    )
    total_sum = convert_price(parser.parse_json(
        json_data, CONSTANT_RECEIPT.get('total_sum'),
    ))
    receipt = Receipt.objects.create(
        receipt_date=receipt_date,
        operation_type=operation_type,
        total_sum=total_sum,
        customer=customer,
    )

    # Getting a list of products
    products_list = parser.parse_json(
        json_data, CONSTANT_RECEIPT.get('items'),
    )

    # Getting an information of products
    result_products_list = []
    for product in products_list:
        product_name = parser.parse_json(
            product, CONSTANT_RECEIPT.get('product_name'),
        )
        price = convert_price(parser.parse_json(
            product, CONSTANT_RECEIPT.get('price'),
        ))
        quantity = parser.parse_json(
            product, CONSTANT_RECEIPT.get('quantity'),
        )
        amount = convert_price(parser.parse_json(
            product, CONSTANT_RECEIPT.get('amount'),
        ))
        nds_type = parser.parse_json(
            product, CONSTANT_RECEIPT.get('nds_type'),
        )
        nds_sum = convert_price(parser.parse_json(
            product, CONSTANT_RECEIPT.get('nds_sum'),
        ))
        products = Product.objects.create(
            product_name=product_name,
            price=price,
            quantity=quantity,
            amount=amount,
            nds_type=nds_type,
            nds_sum=nds_sum,
        )
        result_products_list.append(products)
    receipt.product.set(result_products_list)

    bot_admin.send_message(chat_id, 'Чек принят!')
