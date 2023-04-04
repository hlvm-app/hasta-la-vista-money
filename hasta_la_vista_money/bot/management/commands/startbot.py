from django.core.management import BaseCommand
from hasta_la_vista_money.bot.receipt_parser_json import bot_admin as bot_json
from hasta_la_vista_money.bot.receipt_parser_text import bot_admin as bot_text


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot_json.polling(none_stop=True, skip_pending=False)
        bot_text.polling(none_stop=True, skip_pending=False)
