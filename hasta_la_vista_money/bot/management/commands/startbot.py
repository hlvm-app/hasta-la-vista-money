from django.core.management import BaseCommand
from hasta_la_vista_money.bot.receipt_parser_text import bot_admin as ba_text
from hasta_la_vista_money.bot.receipt_parser_json import bot_admin as ba_json


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
        ba_text.polling(none_stop=True, skip_pending=False)
        ba_json.polling(none_stop=True, skip_pending=False)
