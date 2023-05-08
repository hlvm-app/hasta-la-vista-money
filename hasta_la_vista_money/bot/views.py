from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hasta_la_vista_money.bot.config_bot import bot_admin
from telebot import types

STATUS_SUCCESS = 200
STATUS_BAD = 500


@csrf_exempt
def webhooks(request):
    if request.method == 'POST':
        updates = types.Update.de_json(request.body.decode('utf8'))
        bot_admin.process_new_updates([updates])
        return HttpResponse(
            'Webhook processed successfully', status=STATUS_SUCCESS,
        )
    else:
        return HttpResponse(
            'Webhook URL for Telegram bot', status=STATUS_SUCCESS,
        )
