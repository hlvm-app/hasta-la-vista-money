from telegram import Update
from telegram.ext import CallbackContext

import bot.views
from bot import helpers


def add_receipt(update: Update, context: CallbackContext):
    helpers.receipt_adding_accepted(context.bot, update.effective_chat.id,
                                    bot.views.add_receipt_accepted())
