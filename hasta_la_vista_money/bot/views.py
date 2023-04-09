from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hasta_la_vista_money.bot.config_bot import bot_admin, bot_type
from hasta_la_vista_money.bot.receipt_parser_json import handle_receipt_json
from hasta_la_vista_money.bot.receipt_parser_text import handle_receipt_text


@csrf_exempt
def webhooks(request):
    if request.method == 'POST':
        print(request.headers['Content-Type'])
        json_data = request.body.decode('utf8')
        print(json_data)
        update = bot_type.Update.de_json(json_data)
        print(update)
        handle_receipt_json(update.message)
        handle_receipt_text(update.message)
        bot_admin.process_new_updates([update])
        return HttpResponse('')
