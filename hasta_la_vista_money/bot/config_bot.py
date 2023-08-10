"""Модуль конфигурации бота."""
import os

from dotenv import load_dotenv
from telebot import TeleBot, types
from hasta_la_vista_money.bot.middleware import Middleware


load_dotenv()
token = os.getenv('TOKEN_TELEGRAM_BOT')
bot_admin = TeleBot(token, threaded=False, use_class_middlewares=True)
bot_admin.setup_middleware(Middleware(bot_admin=bot_admin))
bot_type = types
