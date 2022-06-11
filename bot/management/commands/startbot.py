from django.core.management import BaseCommand
import os
from telegram.ext import Updater, MessageHandler, Filters

from bot.telegrambot import get_receipt

TOKEN = os.environ.get('TOKEN_TELEGRAM_BOT')


class Command(BaseCommand):

    def handle(self, *args, **options):
        updater = Updater(token=TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(
            MessageHandler(
                Filters.document.mime_type('application/json'), get_receipt
            )
        )

        updater.start_polling()
        updater.idle()
