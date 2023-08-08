import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hasta_la_vista_money.bot.bot_handler import (
    handle_receipt,
    handle_select_account,
    handle_start,
)
from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.bot.log_config import logger
from hasta_la_vista_money.constants import HTTPStatus, ResponseText
from telebot import types

bot_admin.add_message_handler(handle_receipt)
bot_admin.add_message_handler(handle_start)
bot_admin.add_callback_query_handler(handle_select_account)


@csrf_exempt
def webhooks(request) -> HttpResponse:
    """
    Функция принятия сообщений от телеграм сервера (бота).

    :param request:
    :return: HttpResponse
    """
    if request.method == 'POST':
        json_data = json.loads(request.body)
        try:
            update = types.Update.de_json(json_data)
            bot_admin.process_new_updates([update])
            return HttpResponse(
                ResponseText.SUCCESS_WEBHOOKS.value,
                status=HTTPStatus.SUCCESS_CODE.value,
            )
        except Exception as error:
            logger.error(error)

    return HttpResponse(
        ResponseText.WEBHOOKS_TELEGRAM.value,
        status=HTTPStatus.SUCCESS_CODE.value,
    )
