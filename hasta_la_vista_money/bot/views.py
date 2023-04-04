from django.http import HttpResponse

from .config_bot import bot_admin
from .config_bot import bot_type


def webhooks(request):
    if request.method == 'POST':
        json_data = request.body.decode('utf-8')
        update = bot_type.Update.de_json(json_data)
        bot_admin.process_new_updates([update])
        return HttpResponse('')
