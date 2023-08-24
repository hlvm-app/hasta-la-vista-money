"""Модуль задач для пакета bot."""
import json
from celery import shared_task
from hasta_la_vista_money.bot.receipt_api_receiver import ReceiptApiReceiver
from hasta_la_vista_money.bot.receipt_parse import ReceiptParser
from hasta_la_vista_money.users.models import User


@shared_task
def async_handle_receipt_text_qrcode(
    chat_id,
    user_id,
    account,
    input_user,
):
    """
    Функция-задача celery для обработки сообщений от пользователя.

    Обрабатывается текст из QR-кода.

    :param chat_id:
    :param user_id:
    :param account:
    :param input_user:
    :return:
    """
    user = User.objects.get(id=user_id)
    client = ReceiptApiReceiver()
    json_data = client.get_receipt(input_user)
    parse = ReceiptParser(json_data, user, account)
    parse.parse_receipt(chat_id)


@shared_task
def async_handle_receipt_json(
    chat_id,
    user_id,
    account,
    json_data,
):
    """
    Функция-задача celery для обработки json файлов от пользователя.

    :param chat_id:
    :param user_id:
    :param account:
    :param json_data:
    :return:
    """
    user = User.objects.get(id=user_id)
    parse = ReceiptParser(json_data, user, account)
    parse.parse_receipt(chat_id)
    