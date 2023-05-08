import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hasta_la_vista_money.bot.config_bot import bot_admin, bot_type
from hasta_la_vista_money.bot.log_config import logger


@csrf_exempt
def webhooks(request):
    if request.method == 'POST':
        try:
            print(request)
            print(request.body)
            print(json.loads(request.body))
            print(request.content_type)
            print(request.POST)
            json_data = request.body.decode('utf8')
            updates = bot_type.Update.de_json(json_data)
            bot_admin.process_new_updates([updates])
            return HttpResponse('Webhook processed successfully', status=200)
        except Exception as error:
            logger.error(error)
            return HttpResponse(status=500)
    else:
        return HttpResponse('Webhook URL for Telegram bot', status=200)
