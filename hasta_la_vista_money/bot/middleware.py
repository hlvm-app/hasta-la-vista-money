from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.constants import TelegramMessage
from hasta_la_vista_money.users.models import TelegramUser
from telebot.handler_backends import BaseMiddleware, SkipHandler


class AccessMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.telegram_username = None
        self.update_types = ['message']

    def pre_process(self, message, data):  # noqa: WPS110
        self.telegram_username = TelegramUser.objects.filter(
            telegram_id=message.from_user.id,
        ).first()
        if message.text and (
            '/auth' in message.text
            or '/start' in message.text
            or '/help' in message.text
        ):
            return None

        if self.telegram_username is None and message.text:
            bot_admin.send_message(
                message.chat.id,
                TelegramMessage.ACCESS_DENIED.value,
            )
            return SkipHandler()

    def post_process(self, message, data, exception):  # noqa: WPS110
        data['exception'] = exception
