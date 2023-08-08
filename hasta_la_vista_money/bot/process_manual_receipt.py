from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.users.models import TelegramUser

dictionary_string_from_qrcode = {}


@bot_admin.message_handler(commands=['manual'])
def start_process_add_manual_receipt(message):
    """
    Функция обработчик команды manual.

    :param message:
    :return:
    """
    telegram_username = message.from_user.username
    existing_telegram_user = TelegramUser.objects.filter(
        username=telegram_username,
    ).first()
    if existing_telegram_user:
        bot_admin.send_message(message.chat.id, '')
