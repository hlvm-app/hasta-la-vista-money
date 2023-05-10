"""Модуль декодирования изображения QR-кода в текст."""
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
        return decode_image[0].data.decode()

        # Выводим текст из QR-кода
    except IndexError:
        logger.error(
            'QR-код не считался, '
            'попробуй ещё раз или '
            'воспользуйся сторонним приложением '
            'и передай текст из QR-кода боту'  # noqa: C812
        )
    except FileNotFoundError:
        logger.error('Файл не загрузился, попробуйте ещё раз!')
    except Exception as error:
        logger.error(error)
