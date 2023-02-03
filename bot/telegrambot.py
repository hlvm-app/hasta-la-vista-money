import json
import logging
import datetime

# from bot.add_receipt import get_receipt_date, get_receipt_total, \
#     get_receipt_products, get_receipt_seller, add_result_db
from bot.markup import markup
from bot.services import remove_json_file, parse_json_file, convert_price
from receipts.models import Customer, Receipt, Product
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
                goods = Product.objects.create(
                    product_name=item['name'],
                    price=convert_price(item['price']),
                    quantity=item['quantity'],
                    amount=convert_price(item['sum']),
                )
                products.append(goods)
            receipt.product.set(products)

            bot_admin.send_message(message.chat.id, 'Чек принят!')

        remove_json_file('bot/receipt/')

    except FileNotFoundError as error:
        logger.error(
            f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
            f'произошла ошибка: {error}. Файл json не удалился'
        )
    except json.decoder.JSONDecodeError as error:
        logger.error(
            f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
            f'произошла ошибка JSON файла: {error}'
        )
    except Exception as error:
        logger.error(
            f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} '
            f'произошла ошибка: {error}'
        )


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

# ПЕРЕДЕЛАТЬ!
# @bot_admin.callback_query_handler(func=lambda call: True) """ This function
# is a callback handler for handling inline button clicks in a telegram bot.
# It executes the corresponding function based on the value of the button
# click data.
#
# Input: call: CallbackQuery object from the telegram bot API, containing
# information on the button click event.
#
# Output: Sends a message to the chat asking for specific information (e.g.
# date, seller, total, products), or confirms receipt addition to the database.
#
# Handlers: 'date': prompts the user to input the receipt date and calls
# get_receipt_date function 'seller': prompts the user to input the receipt
# seller and calls get_receipt_seller function 'total': prompts the user to
# input the receipt total and calls get_receipt_total function 'products':
# prompts the user to input the receipt products and calls
# get_receipt_products function
#
# Result: Sends a message to the chat confirming receipt addition to the
# database and calls add_result_db function.
#
# :param call: The callback query object containing the callback data,
# message and other metadata. :type call: telegram.CallbackQuery
#
# :return: None
# """
# def callback_add_receipt(call):
#     data = call.data
#     message = call.message
#     handlers = {
#         'date': ('Введи дату', get_receipt_date),
#         'seller': ('Введи имя продавца', get_receipt_seller),
#         'total': ('Введи итоговую сумму чека', get_receipt_total),
#         'products': ('Введи информацию о продуктах', get_receipt_products),
#     }
#     result = {
#         'result': 'Чек будет добавлен в базу данных!',
#     }
#     if data in handlers:
#         bot_admin.send_message(message.chat.id, handlers[data][0])
#         bot_admin.register_next_step_handler(message, handlers[data][1])
#     if data in result:
#         bot_admin.send_message(message.chat.id, result[data])
#         add_result_db(message)
# def process_values(message):
#     # Process the values filled in by the user
#     while True:
#         if message == 'stop':
#             break
#         else:
#             values = message.text.split()
#             print(values)
#
#
# @bot_admin.callback_query_handler(func=lambda call: call.data == 'fill_values')
# def callback_fill_values(call):
#     # Ask the user to fill in the values
#     bot_admin.send_message(chat_id=call.message.chat.id,
#                            text="Please fill in the values:")
#     bot_admin.register_next_step_handler(call.message, process_values)
