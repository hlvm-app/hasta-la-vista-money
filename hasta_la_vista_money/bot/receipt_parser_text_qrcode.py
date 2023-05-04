"""
Модуль для обработки сообщения от пользователя бота.

От пользователя будет ожидаться картинка с QR-кодом.
"""
from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.bot.decode_qrcode import decode_qrcode
from hasta_la_vista_money.bot.json_parse import ReceiptParser
from hasta_la_vista_money.bot.services import ReceiptApiReceiver


@bot_admin.message_handler(content_types=['photo'])
def handle_receipt_text_qrcode(message):
    """
    Функция по обработке сообщения от пользователя.

    Пользователь отправляет картинку или фотографию с изображением QR-кода.
    В `qr_code_file_id` записывается ID файла.
    Затем Byte код изображения записывается в переменную `byte_code`, который
    декодируется в функции `decode_qrcode`.
    Далее, полученный текст из QR-кода, записывается в переменную `text_qr_code`
    и обрабатывается классом `ReceiptApiReceiver`.
    Получаем JSON текст из базы налоговой и парсим через класс `ReceiptParser`.

    АРГУМЕНТЫ:

    message (telegram.MESSAGE): Объект сообщения, содержащий текст,
    отправленный пользователем.
    """
    qr_code_file_id = bot_admin.get_file(message.photo[-1].file_id)
    byte_code = bot_admin.download_file(
        file_path=qr_code_file_id.file_path,
    )
    text_qr_code = decode_qrcode(byte_code)

    json_data = ReceiptApiReceiver().get_receipt(text_qr_code)

    parse = ReceiptParser(json_data)
    parse.parse(message.chat.id)
