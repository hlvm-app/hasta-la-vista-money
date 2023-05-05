"""Модуль конфигурации бота."""

import os
from telebot.async_telebot import AsyncTeleBot, types
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN_TELEGRAM_BOT')
bot_admin = AsyncTeleBot(token, parse_mode='html')
bot_type = types
