import os
import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.executor import start_webhook

import asyncio
from dotenv import load_dotenv

from services import convert_date, convert_time, get_result_price

load_dotenv()
API_TOKEN = os.getenv('TOKEN_TELEGRAM_BOT')
admin_id = os.getenv('ADMIN_ID')
loop = asyncio.get_event_loop()
bot = Bot(API_TOKEN)
dp = Dispatcher(bot, loop=loop)


# HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
#
# # webhook settings
# WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
# WEBHOOK_PATH = f'/api-telegram-hook/{API_TOKEN}'
# WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
#
# # webserver settings
# WEBAPP_HOST = '0.0.0.0'
# WEBAPP_PORT = os.getenv('PORT', default=8000)


# Сообщение для администратора, что бот запущен
async def on_startup(dispatcher):
    await bot.send_message(chat_id=admin_id, text='Бот запущен!\n')
    # await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.send_message(chat_id=admin_id, text='Бот остановлен!\n')
    # await bot.delete_webhook()


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dispatcher=dp,
                           skip_updates=False,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           )
