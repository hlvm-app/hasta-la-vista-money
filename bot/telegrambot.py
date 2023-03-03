import json
import os
import datetime
import re
import tempfile

import telebot

from bot.services import convert_price, \
    convert_date_time, \
    ReceiptApiReceiver, \
    ParseJson
from hasta_la_vista_money.receipts.models import Customer, Receipt, Product
from .log_config import logger, TelegramLogsHandler

token = os.environ.get('TOKEN_TELEGRAM_BOT')
bot_admin = telebot.TeleBot(token, parse_mode='html')
id_group_user = os.environ.get('ID_GROUP_USER')

logger.addHandler(TelegramLogsHandler(bot_admin, id_group_user))


CONSTANT_RECEIPT = {
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
    'items': 'items'
}


def parse_receipt(json_data, chat_id):
    parser = ParseJson(json_data)

    # Getting of receipt items without products
    name_seller = parser.parse_json(
        json_data, CONSTANT_RECEIPT.get('name_seller')
    )
    retail_place_address = parser.parse_json(
        json_data, CONSTANT_RECEIPT.get('retail_place_address')
    )
    retail_place = parser.parse_json(
        json_data, CONSTANT_RECEIPT.get('retail_place')
    )
    customer = Customer.objects.create(
        name_seller=name_seller,
        retail_place_address=retail_place_address,
        retail_place=retail_place
    )

    receipt_date = convert_date_time(parser.parse_json(
        json_data, CONSTANT_RECEIPT.get('receipt_date')
    ))
    operation_type = parser.parse_json(
        json_data, CONSTANT_RECEIPT.get('operation_type')
    )
    total_sum = convert_price(parser.parse_json(
        json_data, CONSTANT_RECEIPT.get('total_sum')
    ))
    receipt = Receipt.objects.create(
        receipt_date=receipt_date,
        operation_type=operation_type,
        total_sum=total_sum,
        customer=customer
    )

    # Getting a list of products
    products_list = parser.parse_json(
        json_data, CONSTANT_RECEIPT.get('items')
    )

    # Getting an information of products
    result_products_list = []
    for product in products_list:
        print(product, type(product))
        product_name = parser.parse_json(
            product, CONSTANT_RECEIPT.get('product_name')
        )
        price = convert_price(parser.parse_json(
            product, CONSTANT_RECEIPT.get('price')
        ))
        quantity = parser.parse_json(
            product, CONSTANT_RECEIPT.get('quantity')
        )
        amount = convert_price(parser.parse_json(
            product, CONSTANT_RECEIPT.get('amount')
        ))
        nds_type = parser.parse_json(
            product, CONSTANT_RECEIPT.get('nds_type')
        )
        nds_sum = parser.parse_json(
            product, CONSTANT_RECEIPT.get('nds_sum')
        )
        products = Product.objects.create(
            product_name=product_name,
            price=price,
            quantity=quantity,
            amount=amount,
            nds_type=nds_type,
            nds_sum=nds_sum
        )
        result_products_list.append(products)
    receipt.product.set(result_products_list)

    bot_admin.send_message(chat_id, 'Чек принят!')


@bot_admin.message_handler(content_types=['document'])
def get_receipt(message):
    if message.document.mime_type != 'application/json':
        bot_admin.send_message(message.chat.id,
                               'Файл должен быть только в формате JSON!')
        return
    try:
        file_info = bot_admin.get_file(message.document.file_id)
        file_downloaded = bot_admin.download_file(
            file_path=file_info.file_path
        )

        with tempfile.NamedTemporaryFile(suffix='.json') as temp_json_file:
            temp_json_file.write(file_downloaded)
            temp_json_file.seek(0)
            json_data = json.load(temp_json_file)

            parse_receipt(json_data, message.chat.id)

    except (FileNotFoundError, json.decoder.JSONDecodeError) as error:
        logger.error(
            f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S} произошла ошибка: '
            f'{error}.'
        )


@bot_admin.message_handler(content_types=['text'])
def get_receipt_text(message):
    input_user = message.text
    pattern = r't=[0-9]{8}T[0-9]{4}' \
              r'&s=[0-9]{1,100}.[0-9]{1,2}&fn=[0-9]{14,17}' \
              r'&i=[0-9]{5,10}&fp=[0-9]{5,12}&n=[0-5]{1}'
    text_pattern = re.match(pattern, input_user)
    if text_pattern:
        try:
            client = ReceiptApiReceiver()
            qr_code = input_user
            json_data = client.get_receipt(qr_code)

            parse_receipt(json_data, message.chat.id)

        except ValueError as value_error:
            bot_admin.send_message(message.chat.id, str(value_error))
    else:
        bot_admin.send_message(message.chat.id, 'Недопустимый текст')
