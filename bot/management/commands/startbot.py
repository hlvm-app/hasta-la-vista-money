from django.core.management import BaseCommand
from bot.settings_bot import bot_admin


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot_admin.polling(none_stop=True, skip_pending=False)
