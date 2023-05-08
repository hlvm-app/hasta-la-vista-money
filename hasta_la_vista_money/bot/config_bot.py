"""Модуль конфигурации бота."""
import os

from telebot import TeleBot, types
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN_TELEGRAM_BOT')
bot_admin = TeleBot(token, parse_mode='html')
bot_type = types
