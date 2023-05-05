from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.bot.receipt_parser_json import handle_receipt_json
from hasta_la_vista_money.bot.receipt_parser_text import handle_receipt_text
from hasta_la_vista_money.bot.receipt_parser_text_qrcode import \
    handle_receipt_text_qrcode


@bot_admin.message_handler(
    func=lambda message: True, content_types=['text', 'document', 'photo']
)
async def handler(message):
    if message.content_type == 'text':
        handle_receipt_text(message, bot_admin)
    elif message.content_type == 'photo':
        handle_receipt_text_qrcode(message, bot_admin)
    elif message.content_type == 'document':
        handle_receipt_json(message, bot_admin)
    else:
        bot_admin.send_message(
            message.chat.id,
            'Принимаются файлы JSON, текст по формату и фотографии QR-кодов'
        )
