from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.bot.receipt_parser_json import handle_receipt_json
from hasta_la_vista_money.bot.receipt_parser_text import handle_receipt_text
from hasta_la_vista_money.bot.receipt_parser_text_qrcode import (
    handle_receipt_text_qrcode,
)
from hasta_la_vista_money.constants import TelegramMessage


def telegram_content_type(message, user, account):
    """
    Обработка сообщений по типу контента от пользователя.

    :param message:
    :param user:
    :param account:
    :return:
    """
    if message.content_type == 'text':
        handle_receipt_text(message, bot_admin, user, account)
    elif message.content_type == 'photo':
        handle_receipt_text_qrcode(message, bot_admin, user, account)
    elif message.content_type == 'document':
        handle_receipt_json(message, bot_admin, user, account)
    else:
        bot_admin.send_message(
            message.chat.id,
            TelegramMessage.ACCEPTED_FORMAT_JSON.value,
        )
