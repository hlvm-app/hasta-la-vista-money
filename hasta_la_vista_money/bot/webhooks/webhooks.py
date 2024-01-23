import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hasta_la_vista_money import constants
from hasta_la_vista_money.bot.bot_handler.bot_commands_handler import (
    handle_receipt,
    handle_select_account,
    handle_start,
    start_process_add_manual_receipt,
)
from hasta_la_vista_money.bot.config_bot.config_bot import bot_admin
from hasta_la_vista_money.bot.log_config import logger
from telebot import types

bot_admin.add_message_handler(handle_receipt)
bot_admin.add_message_handler(handle_start)
bot_admin.add_message_handler(start_process_add_manual_receipt)
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
                constants.SUCCESS_WEBHOOKS,
                status=constants.SUCCESS_CODE,
            )
        except TypeError:
            # Скрываем ошибку 'function' object is not subscriptable.
            # Закрепление сообщения в личной переписке
            # пользователя с ботом не поддерживается телеграмом. Но работает :)
            pass  # noqa: WPS420
        except Exception as error:
            logger.error(error)

    return HttpResponse(
        constants.WEBHOOKS_TELEGRAM,
        status=constants.SUCCESS_CODE,
    )
