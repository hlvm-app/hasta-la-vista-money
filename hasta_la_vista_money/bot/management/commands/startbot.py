from django.core.management import BaseCommand
from hasta_la_vista_money.bot.receipt_parser_json import bot_admin as bot_json
from hasta_la_vista_money.bot.receipt_parser_text import bot_admin as bot_text


class Command(BaseCommand):
    """
        Django команда для запуска ботов.
        Разбирает чеки и взаимодействуют с пользователем через Telegram.



        Методы:
            - handle(self, *args, **options): Метод, который запускает ботов, которые разбирают чеки и взаимодействуют
            с пользователем через Telegram. Использует bot_admin из hasta_la_vista_money.bot.receipt_parser_json для парсинга
            JSON-файлов и bot_admin из hasta_la_vista_money.bot.receipt_parser_text для парсинга текстовых сообщений.
        """
    def handle(self, *args, **options):
        """
        Метод, который запускает ботов.

        Использует bot_admin из hasta_la_vista_money.bot.receipt_parser_json
        для парсинга JSON-файлов и bot_admin из
        hasta_la_vista_money.bot.receipt_parser_text
        для парсинга текстовых сообщений.

        :param args:
        :param options:
        :return: None
        """
        bot_json.polling(none_stop=True, skip_pending=False)
        bot_text.polling(none_stop=True, skip_pending=False)
