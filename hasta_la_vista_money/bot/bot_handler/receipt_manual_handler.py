import os

import requests
from dateutil.parser import parse
from hasta_la_vista_money.bot.config_bot.config_bot import bot_admin
from hasta_la_vista_money.bot.receipt_handler.receipt_parser import (
    ReceiptParser,
)
from hasta_la_vista_money.bot.services import get_telegram_user
from hasta_la_vista_money.constants import (
    CANCEL_MANUAL_RECEIPT,
    START_MANUAL_HANDLER_RECEIPT,
)
from telebot.handler_backends import State, StatesGroup


class ReceiptStates(StatesGroup):
    date = State()
    amount = State()
    fn = State()
    fd = State()
    fp = State()


@bot_admin.message_handler(commands=['manual'])
def manual_handler_receipt(message):
    """Start handler command manual."""
    if message:
        bot_admin.set_state(
            message.from_user.id,
            ReceiptStates.date,
            message.chat.id,
        )
        bot_admin.send_message(message.chat.id, START_MANUAL_HANDLER_RECEIPT[:])


@bot_admin.message_handler(state='*', commands=['cancel'])
def any_state(message):
    """Cancel state."""
    bot_admin.send_message(message.chat.id, CANCEL_MANUAL_RECEIPT)
    bot_admin.delete_state(message.from_user.id, message.chat.id)


@bot_admin.message_handler(state=ReceiptStates.date)
def receipt_date_get(message):
    """Handle receipt date."""
    bot_admin.send_message(message.chat.id, 'Введите сумму чека')
    bot_admin.set_state(
        message.from_user.id,
        ReceiptStates.amount,
        message.chat.id,
    )
    with bot_admin.retrieve_data(message.from_user.id, message.chat.id) as data:
        date = parse(message.text)
        data['date'] = f'{date:%Y%m%dT%H%M%S}'


@bot_admin.message_handler(state=ReceiptStates.amount)
def receipt_amount_get(message):
    """Handle receipt amount."""
    bot_admin.send_message(message.chat.id, 'Введите номер ФН')
    bot_admin.set_state(
        message.from_user.id,
        ReceiptStates.fn,
        message.chat.id,
    )
    with bot_admin.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['amount'] = message.text


@bot_admin.message_handler(state=ReceiptStates.fn)
def receipt_fn_get(message):
    """Handle receipt fn."""
    bot_admin.send_message(message.chat.id, 'Введите номер ФД')
    bot_admin.set_state(
        message.from_user.id,
        ReceiptStates.fd,
        message.chat.id,
    )
    with bot_admin.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['fn'] = message.text


@bot_admin.message_handler(state=ReceiptStates.fd)
def receipt_fd_get(message):
    """Handle receipt fd."""
    bot_admin.send_message(message.chat.id, 'Введите номер ФП')
    bot_admin.set_state(
        message.from_user.id,
        ReceiptStates.fp,
        message.chat.id,
    )
    with bot_admin.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['fd'] = message.text


@bot_admin.message_handler(state=ReceiptStates.fp)
def receipt_fp_get(message):
    """Handle receipt fp and result send user and record to database info."""
    with bot_admin.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg = f't={data["date"]}&s={data["amount"]}&fn={data["fn"]}&i={data["fd"]}&fp={message.text}&n=1'  # noqa: E501, WPS221
        bot_admin.send_message(
            message.chat.id,
            f'Получилась строка:\n{msg[0]}',
            parse_mode='html',
        )
        telegram_user = get_telegram_user(message)
        if telegram_user:
            user = telegram_user.user
            account = telegram_user.selected_account_id
            data = {
                'token': os.getenv('TOKEN', None),
                'qrraw': msg,
            }
            url = 'https://proverkacheka.com/api/v1/check/get'
            response = requests.post(url, data=data, timeout=10)
            json_data = response.json()
            parser = ReceiptParser(json_data, user, account)
            parser.parse_receipt(message.chat.id)
    bot_admin.delete_state(message.from_user.id, message.chat.id)
