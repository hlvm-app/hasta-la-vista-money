from bot.receipt_parser_json import bot_admin as bot_json
from bot.receipt_parser_text import bot_admin as bot_text
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot_json.polling(none_stop=True, skip_pending=False)
        bot_text.polling(none_stop=True, skip_pending=False)
