from django.http import HttpResponse, HttpResponseNotAllowed
from django.middleware import csrf
from hasta_la_vista_money.bot.config_bot import bot_admin, bot_type
from hasta_la_vista_money.bot.receipt_parser_json import handle_receipt_json
from hasta_la_vista_money.bot.receipt_parser_text import handle_receipt_text


def webhooks(request):
    if request.method == 'POST':
        # Get the CSRF token from the request cookies
        csrf_token = request.COOKIES.get('csrftoken')
        # Create the headers with the CSRF token
        headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        }
        # Get the JSON data from the request body
        json_data = request.body.decode('utf8')
        try:
            update = bot_type.Update.de_json(json_data)
            bot_admin.process_new_updates([update])
            return HttpResponse('Webhook processed successfully')
        except Exception as error:
            return HttpResponse(error, status=500)
    else:
        return HttpResponseNotAllowed(['POST'])
