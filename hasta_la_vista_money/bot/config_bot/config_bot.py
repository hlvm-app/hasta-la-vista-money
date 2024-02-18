"""Модуль конфигурации бота."""
import logging
import os

from dotenv import load_dotenv
from telebot import TeleBot, logger, types
from telebot.storage import StateMemoryStorage

load_dotenv()
token = os.getenv('TOKEN_TELEGRAM_BOT')
if os.getenv('DEBUG'):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
state_storage = StateMemoryStorage()
bot_admin = TeleBot(
    token,
    threaded=False,
    use_class_middlewares=True,
    parse_mode='html',
    state_storage=state_storage,
)
bot_type = types
