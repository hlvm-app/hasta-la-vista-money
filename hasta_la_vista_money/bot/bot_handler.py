from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.bot.receipt_parser_json import handle_receipt_json
from hasta_la_vista_money.bot.receipt_parser_text import handle_receipt_text
from hasta_la_vista_money.bot.receipt_parser_text_qrcode import \
    handle_receipt_text_qrcode


# Обработка команды /start
@bot_admin.message_handler(commands=['start'])
def start_message(message):
    bot_admin.reply_to(message, "Привет! Я бот!")


# Обработка текстовых сообщений
@bot_admin.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot_admin.reply_to(message, message.text)

# @bot_admin.message_handler(content_types=['text', 'document', 'photo'])
# def handler(message):
#     if message.content_type == 'text':
#         handle_receipt_text(message, bot_admin)
#     elif message.content_type == 'photo':
#         handle_receipt_text_qrcode(message, bot_admin)
#     elif message.content_type == 'document':
#         handle_receipt_json(message, bot_admin)
#     else:
#         bot_admin.send_message(
#             message.chat.id,
#             'Принимаются файлы JSON, текст по формату и фотографии QR-кодов'
#         )
