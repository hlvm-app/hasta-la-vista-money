import json
import os
import datetime
import re
import tempfile

import telebot

from bot.services import convert_price, convert_date_time, ReceiptApiReceiver, \
    get_value
from hasta_la_vista_money.receipts.models import Customer, Receipt, Product
from .log_config import logger, TelegramLogsHandler

token = os.environ.get('TOKEN_TELEGRAM_BOT')
bot_admin = telebot.TeleBot(token, parse_mode='html')
id_group_user = os.environ.get('ID_GROUP_USER')

logger.addHandler(TelegramLogsHandler(bot_admin, id_group_user))


CONSTANT_RECEIPT = {
    'seller': 'user',
    'retail_place_address': 'retailPlaceAddress',
    'retail_place': 'retailPlace',
    'date_time': 'dateTime',
    'operation_type': 'operationType',
    'total_sum': 'totalSum',
    'product_name': 'name',
    'price': 'price',
    'quantity': 'quantity',
    'amount': 'sum',
    'nds_type': 'nds',
    'nds_sum': 'ndsSum'
}


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

            customer = Customer.objects.create(
                name_seller=json_data.get(CONSTANT_RECEIPT['seller']),
                retail_place_address=json_data.get(
                    CONSTANT_RECEIPT['retail_place_address']
                ),
                retail_place=json_data.get(CONSTANT_RECEIPT['retail_place']),
            )

            receipt = Receipt.objects.create(
                receipt_date=json_data.get(CONSTANT_RECEIPT['date_time']),
                operation_type=json_data.get(
                    CONSTANT_RECEIPT['operation_type']
                ),
                total_sum=json_data.get(CONSTANT_RECEIPT['total_sum']),
                customer=customer,
            )

            products = []
            for item in json_data['items']:
                product_name = item.get(
                    CONSTANT_RECEIPT['product_name'], 'Нет данных'
                )
                price = convert_price(item.get(CONSTANT_RECEIPT['price'], 0))
                quantity = item.get(CONSTANT_RECEIPT['quantity'], 0)
                amount = convert_price(item.get(CONSTANT_RECEIPT['amount'], 0))
                nds_type = item.get(CONSTANT_RECEIPT['nds_type'], -1)
                nds_sum = item.get(CONSTANT_RECEIPT['nds_sum'], 0)
                goods = Product.objects.create(
                    product_name=product_name,
                    price=price,
                    quantity=quantity,
                    amount=amount,
                    nds_type=nds_type,
                    nds_sum=nds_sum
                )
                products.append(goods)
            receipt.product.set(products)

            bot_admin.send_message(message.chat.id, 'Чек принят!')

    except (FileNotFoundError, json.decoder.JSONDecodeError) as error:
        logger.error(
            f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S} произошла ошибка: '
            f'{error}.'
        )
    except Exception as error:
        logger.error(
            f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S} произошла ошибка: '
            f'{error}'
        )


@bot_admin.message_handler(content_types=['text'])
def get_receipt_text(message):
    input_user = message.text
    pattern = r't=[0-9]{8}T[0-9]{4}' \
              r'&s=[0-9]+.[0-9]+&fn=[0-9]{16}&i=[0-9]+&fp=[0-9]{9}&n=[0-9]'
    text_pattern = re.match(pattern, input_user)
    if text_pattern:
        try:
            client = ReceiptApiReceiver()
            qr_code = input_user
            receipt = client.get_receipt(qr_code)
            json_data_dumps = json.dumps(receipt, ensure_ascii=False)
            json_data_load = json.loads(json_data_dumps)

            date_time = convert_date_time(
                get_value(json_data_load, CONSTANT_RECEIPT['date_time'])
            )
            print(date_time, 'date_time')

        except ValueError as value_error:
            bot_admin.send_message(message.chat.id, str(value_error))
    else:
        bot_admin.send_message(message.chat.id, 'Недопустимый текст')
