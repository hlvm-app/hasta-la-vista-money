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


# Сообщение для администратора, что бот запущен
async def on_startup(dispatcher):
    await bot.send_message(chat_id=admin_id, text='Бот запущен!\n')


async def on_shutdown(dispatcher):
    await bot.send_message(chat_id=admin_id, text='Бот остановлен!\n')


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
