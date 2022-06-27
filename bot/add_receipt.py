import os

import telebot
from receipts.models import Receipt

token = os.environ.get('TOKEN_TELEGRAM_BOT')
bot_admin = telebot.TeleBot(token, parse_mode='html')


result = []


def get_receipt_date(message):
    date = message.text
    result.append(date)


def get_receipt_seller(message):
    seller = message.text
    result.append(seller)


def get_receipt_total(message):
    total = message.text
    result.append(total)


def get_receipt_products(message):
    info = message.text
    result_info = info.split(';', maxsplit=-1)
    result.append(result_info)


def add_result_db(message):
    list2 = []
    for item in result[3]:
        list2.append(item.split(','))
    Receipt.objects.create(
        receipt_date=result[0],
        name_seller=result[1],
        total_sum=result[2],
        product_information=list2
    )
    bot_admin.send_message(message.chat.id, 'Чек добавлен!')
