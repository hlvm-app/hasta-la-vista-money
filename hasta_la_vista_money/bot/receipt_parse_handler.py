from django.shortcuts import get_object_or_404
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.bot.send_message.send_message_tg_user import (
    SendMessageToTelegramUser,
)
from hasta_la_vista_money.constants import TelegramMessage
from hasta_la_vista_money.receipts.models import Receipt


def get_string_result_receipt(account, product_list, receipt_date, customer):
    """
    Формирование строки с краткой информацией о добавленном чеке.

    :param account:
    :param product_list:
    :param receipt_date:
    :param customer:
    :return:
    """
    account_balance = get_object_or_404(Account, id=account)
    products = [product.product_name for product in product_list]
    newline_char = '\n'
    return ''.join(
        (
            'Чек успешно добавлен.\n\n',
            'Параметры чека:\n',
            f'<b>Счёт списания:</b> {account_balance.name_account}\n',
            f'<b>Дата чека:</b> {receipt_date}\n',
            f'<b>Продавец:</b> {customer}\n\n',
            f"<b>Товары:</b>\n{f', {newline_char}'.join(products)}\n",
        ),
    )


def check_exists_number_receipt(user, number_receipt):
    """
    Проверка на существование номера чека в базе данных.

    :param user:
    :param number_receipt:
    :return:
    """
    return Receipt.objects.filter(
        user=user,
        number_receipt=number_receipt,
    ).first()


def check_operation_type(operation_type, total_sum):
    """
    Проверка на тип операции.

    Если это возврат покупки или возврат выигрыша, то это минус со счёта.

    :param operation_type:
    :param total_sum:
    :return:
    """
    return -total_sum if operation_type in {2, 3} else total_sum


def handle_integrity_error(chat_id, integrity_error):
    """
    Обработка исключений.

    :param chat_id:
    :param integrity_error:
    :return:
    """
    if 'account' in str(integrity_error):
        SendMessageToTelegramUser.send_message_to_telegram_user(
            chat_id,
            TelegramMessage.NOT_CREATE_ACCOUNT.value,
        )
    else:
        SendMessageToTelegramUser.send_message_to_telegram_user(
            chat_id,
            TelegramMessage.ERROR_DATABASE_RECORD.value,
        )
