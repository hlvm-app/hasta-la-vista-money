import json
import os
import datetime
import tempfile

import telebot

from bot.services import parse_json_file, convert_price
from hasta_la_vista_money.receipts.models import Customer, Receipt, Product
from .log_config import logger, TelegramLogsHandler

token = os.environ.get('TOKEN_TELEGRAM_BOT')
bot_admin = telebot.TeleBot(token, parse_mode='html')
id_group_user = os.environ.get('ID_GROUP_USER')

logger.addHandler(TelegramLogsHandler(bot_admin, id_group_user))


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
                name_seller=parse_json_file(json_data)[1],
                retail_place_address=parse_json_file(json_data)[3],
                retail_place=parse_json_file(json_data)[5],
            )

            receipt = Receipt.objects.create(
                receipt_date=parse_json_file(json_data)[0],
                operation_type=parse_json_file(json_data)[4],
                total_sum=parse_json_file(json_data)[2],
                customer=customer,
            )

            products = []
            for item in json_data['items']:
                product_name = item.get('name', 'Нет данных')
                price = convert_price(item.get('price', 0))
                quantity = item.get('quantity', 0)
                amount = convert_price(item.get('sum', 0))
                nds_type = item.get('nds', -1)
                nds_sum = item.get('ndsSum', 0)
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
