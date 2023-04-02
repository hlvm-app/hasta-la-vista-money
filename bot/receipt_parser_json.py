import datetime
import json

from bot.config_bot import bot_admin
from bot.json_parse import ReceiptParser
from bot.log_config import logger


@bot_admin.message_handler(content_types=['document'])
def handle_receipt_json(message):
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

        parse = ReceiptParser(json_data)
        parse.parse(message.chat.id)

    except json.decoder.JSONDecodeError as json_error:
        logger.error(
            f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n'
            f'Некорректный JSON файл: {json_error}.\n'
            f'Проверьте тот ли файл загружаете...',
        )
