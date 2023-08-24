"""
Модуль с функцией, которая обрабатывает сообщение от пользователя.

Пользователь при этом должен отправить json файл. Другой тип не принимается.
"""
import datetime
import json

from hasta_la_vista_money.bot.log_config import logger
from hasta_la_vista_money.bot.tasks import async_handle_receipt_json


def handle_receipt_json(message, bot, user, account):
    """
    Функция принимает один аргумент message.

    Функция проверяет, что документ, прикрепленный к сообщению, имеет тип
    application/json. Если это не так, функция отправляет сообщение об ошибке
    пользователю и завершается.
    Если документ корректный, функция скачивает его, парсит содержимое и
    отправляет результат пользователю.

    АРГУМЕНТЫ:

    message: object
        Функция в качестве аргумента принимает объект сообщения от пользователя.

    ИСКЛЮЧЕНИЯ: json.decoder.JSONDecodeError
        Если JSON файл имеет некорректную структуру, программа выбрасывает
        исключение.
    """
    if message.document.mime_type != 'application/json':
        bot.send_message(
            message.chat.id,
            'Файл должен быть только в формате JSON!',
        )
        return
    try:
        file_info = bot.get_file(message.document.file_id)
        file_downloaded = bot.download_file(
            file_path=file_info.file_path,
        )
        chat_id = message.chat.id
        user_id = user.id
        json_data = json.loads(file_downloaded)

        async_handle_receipt_json.delay(
            chat_id=chat_id,
            user_id=user_id,
            account=account,
            json_data=json_data,
        )

    except json.decoder.JSONDecodeError as json_error:
        logger.error(
            ''.join(
                (
                    f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n',
                    f'Некорректный JSON файл: {json_error}.\n',
                    'Проверьте тот ли файл загружаете...',
                ),
            ),
        )
