import json
import logging
import datetime

from bot.add_receipt import get_receipt_date, get_receipt_total, \
    get_receipt_products, get_receipt_seller, add_result_db
from bot.markup import markup
from bot.services import convert_date_time, get_result_price, remove_json_file
from receipts.models import Receipt
import os
import telebot

token = os.environ.get('TOKEN_TELEGRAM_BOT')
bot_admin = telebot.TeleBot(token, parse_mode='html')
id_group_user = os.environ.get('ID_GROUP_USER')


logger = logging.getLogger(__name__)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


logger.addHandler(TelegramLogsHandler(bot_admin, id_group_user))


@bot_admin.message_handler(func=lambda message: message.document.mime_type ==
                           'application/json',
                           content_types=['document'])
def get_receipt(message):
    try:
        file_info = bot_admin.get_file(message.document.file_id)
        file_downloaded = bot_admin.download_file(
            file_path=file_info.file_path
        )
        src = f'bot/receipt/{message.document.file_name}'
        with open(src, 'wb') as file:
            file.write(file_downloaded)

        with open(file.name, 'r') as json_file:
            json_data = json.load(json_file)
            date_time = convert_date_time(json_data["dateTime"])
            seller = json_data['user']
            total_sum = str(get_result_price(json_data["totalSum"]))
            information_products = []

            for item in json_data["items"]:
                name_product = item["name"]
                price = str(get_result_price(item["price"]))
                quantity = str(item["quantity"])
                amount = str(get_result_price(item["sum"]))
                list_product_information = [name_product, price, quantity,
                                            amount]
                information_products.append(list_product_information)

            Receipt.objects.get_or_create(
                receipt_date=date_time,
                name_seller=seller,
                product_information=information_products,
                total_sum=total_sum
            )
            bot_admin.send_message(message.chat.id, 'Чек принят!')
        remove_json_file('bot/receipt/')
    except FileNotFoundError as error:
        logger.error(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                     f'произошла ошибка: {error}. Файл json не удалился')
    except json.decoder.JSONDecodeError as error:
        logger.error(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                     f'произошла ошибка JSON файла: {error}')
    except Exception as error:
        logger.error(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
                     f'произошла ошибка: {error}')


@bot_admin.message_handler(func=lambda message: message.document.mime_type !=
                           'application/json',
                           content_types=['document'])
def not_json_file(message):
    if message.document.mime_type != 'application/json':
        bot_admin.send_message(message.chat.id,
                               'Файл должен быть только в формате JSON!')


@bot_admin.message_handler(commands=['add'])
def add_receipt(message):
    text = message.text
    if text == '/add':
        bot_admin.send_message(message.chat.id, 'Выберите действие:',
                               reply_markup=markup())


@bot_admin.callback_query_handler(func=lambda call: True)
def callback_add_receipt(call):
    data = call.data
    message = call.message
    if data == 'date':
        bot_admin.send_message(message.chat.id, 'Введи дату')
        bot_admin.register_next_step_handler(message, get_receipt_date)
    if data == 'seller':
        bot_admin.send_message(message.chat.id, 'Введи имя продавца')
        bot_admin.register_next_step_handler(message, get_receipt_seller)
    if data == 'total':
        bot_admin.send_message(message.chat.id, 'Введи итоговую сумму чека')
        bot_admin.register_next_step_handler(message, get_receipt_total)
    if data == 'products':
        bot_admin.send_message(message.chat.id, 'Введи информацию о продуктах')
        bot_admin.register_next_step_handler(message, get_receipt_products)
    if data == 'result':
        bot_admin.send_message(message.chat.id,
                               'Чек будет добавлен в базу данных!')
        add_result_db(message)
