"""Модуль декодирования изображения QR-кода в текст."""
import cv2
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
        img = cv2.imread(image)
        detector = cv2.QRCodeDetector()
        text_qrcode, bbox, straight_qrcode = detector.detectAndDecode(img)

        # Выводим текст из QR-кода
        return text_qrcode
    except Exception as error:
        logger.error(error)