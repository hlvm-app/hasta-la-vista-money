from telebot.handler_backends import BaseMiddleware, CancelUpdate
from hasta_la_vista_money.users.models import TelegramUser


class Middleware(BaseMiddleware):
    def __init__(self, bot_admin):
        super().__init__()
        self.bot_admin = bot_admin
        self.telegram_username = None


    def pre_process(self, message, data):
        self.telegram_username = TelegramUser.objects.filter(
            telegram_id=message.from_user.id,
        ).first()
        if not self.telegram_username:
            self.bot_admin.send_message(message.chat.id, 'Access Denied')
            return CancelUpdate()
        return super().pre_process(message, data)