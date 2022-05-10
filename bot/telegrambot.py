import os
import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import asyncio
import json

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


@dp.message_handler(content_types=['document'])
async def get_receipt(message: types.Message):
    json_file = await bot.get_file(message.document['file_id'])
    if json_file.file_path[-4:] == "json":
        downloaded_file = await bot.download_file(json_file.file_path,
                                                  'receipt/receipt.json')
        try:
            with open(f'{downloaded_file.name}', 'r') as read:
                r = json.load(read)

                if 'items' in r:
                    await message.answer(
                        "Спасибо, файл добавлен в базу данных!")

                    print(r)
                else:
                    await message.answer(
                        "Файл не соответствует формату, пришлите корректный "
                        "файл!")
        except json.JSONDecodeError:
            await message.answer(
                "Файл не соответствует формату, пришлите корректный "
                "файл!")

    else:
        await message.answer(
            "Файл не соответствует формату, пришлите корректный файл!")


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    executor.start_polling(dispatcher=dp,
                           skip_updates=False,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           )
