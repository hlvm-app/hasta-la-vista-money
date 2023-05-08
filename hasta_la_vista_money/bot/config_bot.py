"""Модуль конфигурации бота."""
import os

from dotenv import load_dotenv
from telebot import TeleBot, types

load_dotenv()
token = os.getenv('TOKEN_TELEGRAM_BOT')
bot_admin = TeleBot(token, threaded=False)
bot_type = types
