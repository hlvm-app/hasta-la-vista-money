from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.users.models import TelegramUser
from telebot.handler_backends import BaseMiddleware, CancelUpdate


class AccessMiddleware(BaseMiddleware):

    def __init__(self):
        super().__init__()
        self.telegram_username = None
        self.update_types = ['message']

    def pre_process(self, message, data):
        self.telegram_username = TelegramUser.objects.filter(
            telegram_id=message.from_user.id,
        ).first()
        if message.text.startswith('/auth'):
            return super().pre_process(message, data)

        if not self.telegram_username:
            bot_admin.send_message(message.chat.id, 'У вас нет доступа к использованию бота, сначала надо авторизоваться - /auth')
            return CancelUpdate()
        return super().pre_process(message, data)
