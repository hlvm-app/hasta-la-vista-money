from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .config_bot import bot_admin
from .config_bot import bot_type


@csrf_exempt
def webhooks(request):
    if request.method == 'POST':
        json_data = request.body.decode('utf8')
        update = bot_type.Update.de_json(json_data)
        bot_admin.process_new_updates([update])
        return HttpResponse('')
