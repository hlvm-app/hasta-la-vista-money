from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hasta_la_vista_money.bot.config_bot import bot_admin, bot_type
from hasta_la_vista_money.bot.log_config import logger
from hasta_la_vista_money.bot.receipt_parser_json import handle_receipt_json
from hasta_la_vista_money.bot.receipt_parser_text import handle_receipt_text


@csrf_exempt
def webhooks(request):
    if request.method == 'POST':
        json_data = request.body.decode('utf8')
        try:
            update = bot_type.Update.de_json(json_data)
            if update.message.content_type == 'document':
                handle_receipt_json(update.message)
                bot_admin.process_new_updates([update])
            else:
                handle_receipt_text(update.message)
                bot_admin.process_new_updates([update])
            return HttpResponse('Webhook processed successfully')
        except Exception as error:
            logger.error(error)
