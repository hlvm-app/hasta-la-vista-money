from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hasta_la_vista_money.bot.config_bot import bot_admin, bot_type
from hasta_la_vista_money.bot.log_config import logger


@csrf_exempt
def webhooks(request):
    try:
        if request.method == 'POST':
            length = int(request.headers['content-length'])
            json_string = request.body.read(length)
            update = bot_type.Update.de_json(json_string.decode("utf-8"))
            bot_admin.process_new_messages([update.message])
            return HttpResponse('Webhook processed successfully')
    except Exception as error:
        logger.error(error)
