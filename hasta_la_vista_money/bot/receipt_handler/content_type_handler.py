from hasta_la_vista_money.bot.config_bot.config_bot import bot_admin
from hasta_la_vista_money.bot.receipt_handler.receipt_parser_json import (
    handle_receipt_json,
)
from hasta_la_vista_money.bot.receipt_handler.receipt_parser_text import (
    handle_receipt_text,
)
from hasta_la_vista_money.bot.receipt_handler.text_qr_code_handler import (
    handle_receipt_text_qrcode,
)
from hasta_la_vista_money.bot.send_message.send_message_tg_user import (
    SendMessageToTelegramUser,
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
    url = 'https://proverkacheka.com/api/v1/check/get'
    if message.content_type == 'text':
        handle_receipt_text(url, message, bot_admin, user, account)
    elif message.content_type == 'photo':
        handle_receipt_text_qrcode(url, message, bot_admin, user, account)
    elif message.content_type == 'document':
        handle_receipt_json(message, bot_admin, user, account)
    else:
        SendMessageToTelegramUser.send_message_to_telegram_user(
            message.chat.id,
            text=TelegramMessage.ACCEPTED_FORMAT_JSON.value,
        )
