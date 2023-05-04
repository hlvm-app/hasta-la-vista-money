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
            bot_admin.process_new_updates(
                [
                    bot_type.Update.de_json(
                        request.stream.read().decode("utf-8")
                    )
                ]
            )
            return HttpResponse('Webhook processed successfully')
        except Exception as error:
            logger.error(error)
