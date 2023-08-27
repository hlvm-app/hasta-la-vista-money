from django.core.management import BaseCommand
from hasta_la_vista_money.bot.config_bot.config_bot import bot_admin


class Command(BaseCommand):
    """
    Django команда для запуска бота через polling.

    Разбирает чеки и взаимодействуют с пользователем через Telegram.
    """

    def handle(self, *args, **options):
        """
        Метод, который запускает бота через polling.

        Использует bot_admin из hasta_la_vista_money.bot.receipt_parser_json
        для парсинга JSON-файлов и bot_admin из
        hasta_la_vista_money.bot.receipt_parser_text
        для парсинга текстовых сообщений.

        :param args:
        :param options:
        :return: None
        """
        try:
            bot_admin.infinity_polling(none_stop=True, skip_pending=False)
        except TypeError:
            # Заглушка нужна для того, чтобы не выводилась ошибка
            # TypeError: 'function' object is not subscriptable
            # так как чат с ботом не является супергруппой.
            ...
