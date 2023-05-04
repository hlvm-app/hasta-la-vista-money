from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hasta_la_vista_money.bot.config_bot import bot_admin, bot_type
from hasta_la_vista_money.bot.log_config import logger


@csrf_exempt
def webhooks(request):
    print(request.stream)
    print(request.stream.read())
    if request.method == 'POST':
        try:
            json_data = request.get_data().decode('utf-8')
            updates = bot_type.Update.de_json(json_data)
            bot_admin.process_new_updates([updates])
            return HttpResponse('Webhook processed successfully')
        except Exception as error:
            logger.error(error)
