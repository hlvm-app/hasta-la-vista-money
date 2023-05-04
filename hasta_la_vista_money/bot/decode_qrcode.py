"""Модуль декодирования изображения QR-кода в текст."""

import io

import cv2
import numpy as np
from PIL import Image


def decode_qrcode(array_bytes):
    """
    Функцию по декодированию изображения QR-кода в текст.

    :param array_bytes: Байт-код изображения.
    :type array_bytes: bytes
    :return: Строка текста извлеченная из QR-кода.
    :rtype: str
    """
    image = Image.open(io.BytesIO(array_bytes))

    # Преобразуем изображение в массив numpy
    img = np.array(image)

    # Используем cv2 для распознавания QR-кода
    detector = cv2.QRCodeDetector()
    text_qrcode, _, _ = detector.detectAndDecode(img)

    # Выводим текст из QR-кода
    return text_qrcode
