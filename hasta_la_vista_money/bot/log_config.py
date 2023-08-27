import logging
import os

from hasta_la_vista_money.bot.config_bot.config_bot import bot_admin

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        """
        Конструктов класса инициализирующий аргументы класса.

        :param tg_bot:
        :param chat_id:
        """
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def format(self, record: logging.LogRecord) -> str:
        return f'{record.getMessage()}'

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


id_group_user = os.environ.get('ID_GROUP_USER')

logger.addHandler(TelegramLogsHandler(bot_admin, id_group_user))
