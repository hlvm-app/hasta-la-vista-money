from django.core.management import BaseCommand
import os
from bot.telegrambot import bot_admin

TOKEN = os.environ.get('TOKEN_TELEGRAM_BOT')


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot_admin.polling(none_stop=True)
