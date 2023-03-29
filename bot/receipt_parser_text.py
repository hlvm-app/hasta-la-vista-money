import datetime
import re

import requests

from bot.config_bot import bot_admin
from bot.json_parse import ReceiptParser
from bot.log_config import logger
from bot.services import ReceiptApiReceiver


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
        try:
            client = ReceiptApiReceiver()
            qr_code = input_user
            json_data = client.get_receipt(qr_code)

            parse = ReceiptParser(json_data)
            parse.parse(message.chat.id)

        except requests.exceptions.JSONDecodeError as json_error:
            logger.error(
                f'Ошибка обработки json: {json_error}\n'
                f'Время возникновения исключения: '
                f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}'
            )

        except Exception as error:
            logger.error(
                f'{error}Время возникновения исключения: '
                f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}',
            )
    else:
        bot_admin.send_message(message.chat.id, 'Недопустимый текст')
