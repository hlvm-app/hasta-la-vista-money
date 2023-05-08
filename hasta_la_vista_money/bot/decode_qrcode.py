"""Модуль декодирования изображения QR-кода в текст."""
import io

from qrtools import QR
from hasta_la_vista_money.bot.log_config import logger


def decode_qrcode(image):
    """
    Функцию по декодированию изображения QR-кода в текст.

    :param image: Байт-код изображения.
    :type image: photo
    :return: Строка текста извлеченная из QR-кода.
    :rtype: str
    """
    try:
        qr = QR(filename=io.BytesIO(image))
        qr_decode = qr.decode()
        # Выводим текст из QR-кода
        return qr_decode.data
    except Exception as error:
        logger.error(error)


