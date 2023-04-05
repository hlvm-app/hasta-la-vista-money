import re

from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.bot.json_parse import ReceiptParser
from hasta_la_vista_money.bot.log_config import logger
from hasta_la_vista_money.bot.services import ReceiptApiReceiver


@bot_admin.message_handler(content_types=['text'])
def handle_receipt_text(message):
    input_user = message.text

    pattern = (
        r't=[0-9]+T[0-9]+'
        r'&s=[0-9]+.[0-9]+&fn=[0-9]+'
        r'&i=[0-9]+&fp=[0-9]+&n=[0-5]{1}'
    )
    text_pattern = re.match(pattern, input_user)

    if text_pattern:
        client = ReceiptApiReceiver()
        qr_code = input_user
        json_data = client.get_receipt(qr_code)

        parse = ReceiptParser(json_data)
        parse.parse(message.chat.id)
    else:
        bot_admin.send_message(message.chat.id, 'Недопустимый текст')
