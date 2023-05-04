"""Модуль конфигурации бота."""

import os

import telebot
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN_TELEGRAM_BOT')
bot_admin = telebot.TeleBot(token, parse_mode='html')
bot_type = telebot.types
