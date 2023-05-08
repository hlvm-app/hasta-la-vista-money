import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.bot.log_config import logger
from telebot import types

from hasta_la_vista_money.bot.receipt_parser_json import handle_receipt_json
from hasta_la_vista_money.bot.receipt_parser_text import handle_receipt_text

STATUS_SUCCESS = 200


@csrf_exempt
def webhooks(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        try:
            update = types.Update.de_json(json_data)
            bot_admin.process_new_updates([update])
            return HttpResponse('Webhook processed successfully')
        except Exception as error:
            logger.error(error)


