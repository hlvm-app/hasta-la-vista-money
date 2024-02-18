import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hasta_la_vista_money import constants
from hasta_la_vista_money.bot.bot_handler.bot_commands_handler import (
    handle_receipt,
    handle_select_account,
    handle_start,
)
from hasta_la_vista_money.bot.bot_handler.receipt_manual_handler import (
    manual_handler_receipt,
    receipt_amount_get,
    receipt_date_get,
    receipt_fd_get,
    receipt_fn_get,
    receipt_fp_get,
)
from hasta_la_vista_money.bot.config_bot.config_bot import bot_admin
from hasta_la_vista_money.bot.log_config import logger
from telebot import custom_filters, types

bot_admin.add_message_handler(handle_receipt)
bot_admin.add_message_handler(handle_start)
bot_admin.add_message_handler(manual_handler_receipt)
bot_admin.add_message_handler(receipt_date_get)
bot_admin.add_message_handler(receipt_amount_get)
bot_admin.add_message_handler(receipt_fn_get)
bot_admin.add_message_handler(receipt_fd_get)
bot_admin.add_message_handler(receipt_fp_get)
bot_admin.add_callback_query_handler(handle_select_account)
bot_admin.add_custom_filter(custom_filters.StateFilter(bot_admin))


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
