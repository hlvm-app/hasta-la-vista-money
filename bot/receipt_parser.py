import datetime
import json
import re

from bot.config_bot import bot_admin
from bot.json_parse import ReceiptParser
from bot.log_config import logger
from bot.services import ReceiptApiReceiver


@bot_admin.message_handler(content_types=['document'])
def get_receipt(message):
    if message.document.mime_type != 'application/json':
        bot_admin.send_message(
            message.chat.id, 'Файл должен быть только в формате JSON!',
        )
        return
    try:
        file_info = bot_admin.get_file(message.document.file_id)
        file_downloaded = bot_admin.download_file(
            file_path=file_info.file_path,
        )
        json_data = json.loads(file_downloaded)

        parse = ReceiptParser(json_data, message.chat.id)
        parse.parse(message.chat.id)

    except json.decoder.JSONDecodeError as error:
        logger.error(
            f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n'
            f'Некорректный JSON файл: {error}.\n'
            f'Проверьте тот ли файл загружаете...',
        )
    except Exception as error:
        logger.error(
            f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S} произошла ошибка:'
            f' {error}.',
        )


@bot_admin.message_handler(content_types=['text'])
def get_receipt_text(message):
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

            parse = ReceiptParser(json_data, message.chat.id)
            parse.parse(message.chat.id)

        except Exception as error:
            logger.error(
                f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n'
                f'произошла ошибка: {error}.',
            )
    else:
        bot_admin.send_message(message.chat.id, 'Недопустимый текст')
