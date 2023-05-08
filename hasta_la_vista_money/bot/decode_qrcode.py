"""Модуль декодирования изображения QR-кода в текст."""
import io

from PIL import Image
from pyzbar.pyzbar import decode


def decode_qrcode(image_from_bytes):
    result_image = Image.open(io.BytesIO(image_from_bytes))
    return decode(result_image)[0].data.decode()

