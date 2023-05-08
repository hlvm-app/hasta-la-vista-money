import json
from typing import List

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.bot.log_config import logger
from telebot import types, TeleBot

STATUS_SUCCESS = 200
STATUS_BAD = 500


@csrf_exempt
def webhooks(request):
    try:
        if request.method == 'POST':
            update = types.Update.de_json(
                json.loads(request.body.decode('utf8'))
            )
            bot_admin.process_new_updates([update])
            return HttpResponse(
                'Webhook processed successfully', status=STATUS_SUCCESS,
            )
        return HttpResponse(
            'Webhook URL for Telegram bot', status=STATUS_SUCCESS,
            )
    except Exception as error:
        logger.error(error)


class MyBot(TeleBot):
    def process_new_updates(self, updates: List[types.Update]):
        try:
            if not updates:
                logger.error('Not Updates')
            logger.error(updates)
        except Exception as error:
            logger.error(error)
