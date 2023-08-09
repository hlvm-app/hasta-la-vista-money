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
    telegram_user_id = message.from_user.id

    telegram_user = check_telegram_user(telegram_user_id)

    if telegram_user:
        bot_admin.send_message(message.chat.id, 'Чтобы добавить чек используя данные с чека, введите поочередно - дату, ФД, ФП и номер чека. Сначала введите дату в формате ДД-ММ-ГГГГ ЧЧ:ММ')
        bot_admin.register_next_step_handler(message, get_date_receipt)


def get_date_receipt(message):
    dictionary_string_from_qrcode['date'] = message.text
    bot_admin.send_message(message.chat.id, dictionary_string_from_qrcode.items())
