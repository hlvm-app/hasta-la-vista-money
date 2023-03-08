from bot.telegrambot import bot_admin
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot_admin.polling(none_stop=True, skip_pending=False)
