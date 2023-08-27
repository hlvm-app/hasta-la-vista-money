from hasta_la_vista_money.bot.config_bot import bot_admin


class SendMessageToTelegramUser:
    @staticmethod
    def send_message_to_telegram_user(chat_id, text):
        bot_admin.send_message(chat_id, text)
