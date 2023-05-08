"""Модуль конфигурации бота."""
import logging
import os

import telebot
from telebot import TeleBot, types
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN_TELEGRAM_BOT')
bot_admin = TeleBot(token, parse_mode='html')

telebot.logger.setLevel(logging.INFO)
bot_type = types
