"""
Модуль с функцией, которая обрабатывает сообщение от пользователя.

Пользователь при этом должен отправить текст по шаблону, который он получит из
QR-кода чека.
"""
import os
import re

import requests
from hasta_la_vista_money import constants
from hasta_la_vista_money.bot.receipt_handler.receipt_parser import (
    ReceiptParser,
)


def handle_receipt_text(url, message, bot, user, account):
    """
    Обрабатывает текстовые сообщения, содержащие информацию в QR-коде чека.

    Эта функция ожидает получить объект сообщения от пользователя
    Telegram-бота, содержащий строку, соответствующую конкретному шаблону
    для QR-кодов чеков.
    Если шаблон найден, функция использует объект ReceiptApiReceiver
    для получения данных чека и объект ReceiptParser для их обработки.
    Если шаблон не найден, функция отправляет сообщение обратно пользователю,
    указывая на недопустимый текст.

    АРГУМЕНТЫ:

    message (telegram.MESSAGE): Объект сообщения, содержащий текст,
    отправленный пользователем.

    ПРИМЕР:

    "t=20220413T2146&s=63.00&fn=8710000100266677&i=12259&fp=4229365681&n=1"
    """
    input_user = message.text

    pattern = (
        r't=[0-9]+T[0-9]+'
        r'&s=[0-9]+.[0-9]+&fn=[0-9]+'
        r'&i=[0-9]+&fp=[0-9]+&n=[0-5]{1}'
    )
    text_pattern = re.match(pattern, input_user)

    if text_pattern:
        text_qr_code = input_user

        chat_id = message.chat.id

        data = {
            'token': os.getenv('TOKEN', None),
            'qrraw': text_qr_code,
        }
        response = requests.post(url, data=data, timeout=10)
        json_data = response.json()
        if json_data.get('code') != 1:
            bot.send_message(
                message.chat.id,
                constants.NO_INFORMATION_BY_RECEIPT,
            )
            return
        parse = ReceiptParser(json_data, user, account)
        parse.parse_receipt(chat_id)
    else:
        bot.send_message(message.chat.id, 'Недопустимый текст')
