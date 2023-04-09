from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hasta_la_vista_money.bot.config_bot import bot_admin, bot_type


@csrf_exempt
def webhooks(request):
    if request.method == 'POST':
        json_data = request.body.decode('utf8')
        try:
            update = bot_type.Update.de_json(json_data)
            bot_admin.process_new_updates([update])
            return HttpResponse('Webhook processed successfully')
        except Exception as error:
            return HttpResponse(error)
