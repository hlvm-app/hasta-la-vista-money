import asyncio
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hasta_la_vista_money.bot.config_bot import bot_admin, bot_type
from hasta_la_vista_money.bot.log_config import logger


@csrf_exempt
def webhooks(request):
    try:
        if request.method == 'POST':
            json_data = request.body.decode('utf8')
            print(json_data)
            updates = bot_type.Update.de_json(json.loads(json_data))
            print(updates)
            bot_admin.process_new_updates([updates])
            return HttpResponse('Webhook processed successfully')
    except Exception as error:
        logger.error(error)
