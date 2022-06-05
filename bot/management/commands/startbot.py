from django.core.management import BaseCommand
import os

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from bot.telegrambot import get_receipt
from bot.adding_receipt import add_receipt

TOKEN = os.environ.get('TOKEN_TELEGRAM_BOT')


class Command(BaseCommand):
    help = 'Starts the client telegram bot'

    def handle(self, *args, **options):
        updater = Updater(token=TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        button = ['/Add']
        markup = ReplyKeyboardMarkup.from_column(button)

        dispatcher.add_handler(
            MessageHandler(
                Filters.document.mime_type('application/json'), get_receipt
            )
        )
        dispatcher.add_handler(
            CommandHandler(command='Start', callback=add_receipt)
        )

        updater.start_polling()
        updater.idle()
