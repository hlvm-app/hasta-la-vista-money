"""Модуль декодирования изображения QR-кода в текст."""
from PIL import Image
from pyzbar.pyzbar import decode

from hasta_la_vista_money.bot.log_config import logger


def decode_qrcode(image):
    """
    Функцию по декодированию изображения QR-кода в текст.

    :param image: Байт-код изображения.
    :type image: str
    :return: Строка текста извлеченная из QR-кода.
    :rtype: str
    """
    try:
        result = decode(Image.open(image))
        return result[0].data.decode()

        # Выводим текст из QR-кода
    except Exception as error:
        logger.error(error)
