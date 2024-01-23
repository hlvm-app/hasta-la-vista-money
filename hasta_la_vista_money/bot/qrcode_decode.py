"""Модуль декодирования изображения QR-кода в текст."""
from hasta_la_vista_money import constants
from hasta_la_vista_money.bot.log_config import logger
from PIL import Image
from pyzbar.pyzbar import decode


def decode_qrcode(image):
    """
    Функцию по декодированию изображения QR-кода в текст.

    :param image: Байт-код изображения.
    :type image: str
    :return: Строка текста извлеченная из QR-кода.
    :rtype: str
    """
    try:
        decode_image = decode(Image.open(image))

        if len(decode_image) != 0:  # noqa: WPS507
            return decode_image[0].data.decode()
        logger.error(constants.QR_CODE_NOT_CONSIDERED)
        return None

    except FileNotFoundError:
        logger.error('Файл не загрузился, попробуйте ещё раз!')
