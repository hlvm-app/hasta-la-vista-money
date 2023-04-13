"""
Модуль с функцией, которая обрабатывает сообщение от пользователя.

Пользователь при этом должен отправить json файл. Другой тип не принимается.
"""
import datetime
import json

from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.bot.json_parse import ReceiptParser
from hasta_la_vista_money.bot.log_config import logger


@bot_admin.message_handler(content_types=['document'])
def handle_receipt_json(message):
    """
    Функция принимает один аргумент message.

    Функция проверяет, что документ, прикрепленный к сообщению, имеет тип
    application/json. Если это не так, функция отправляет сообщение об ошибке
    пользователю и завершается.
    Если документ корректный, функция скачивает его, парсит содержимое и
    отправляет результат пользователю.

    ПАРАМЕТРЫ:

    message: object
        Функция в качестве аргумента принимает объект сообщения от пользователя.

    ИСКЛЮЧЕНИЯ: json.decoder.JSONDecodeError
        Если JSON файл имеет некорректную структуру, программа выбрасывает
        исключение.
    """
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
