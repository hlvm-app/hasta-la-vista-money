import os

import telebot

token = os.environ.get('TOKEN_TELEGRAM_BOT')
bot_admin = telebot.TeleBot(token, parse_mode='html')
