from hasta_la_vista_money.bot.config_bot import bot_admin


def pin_message(call, account):
    """
    Функция закрепления сообщения.

    :param call:
    :param account:
    :return:
    """
    bot_admin.unpin_all_chat_messages(chat_id=call.message.chat.id)
    pinned_message = bot_admin.send_message(
        chat_id=call.message.chat.id,
        text=f'Выбран счёт: {account.name_account}',
    )
    bot_admin.pin_chat_message(
        chat_id=call.message.chat.id,
        message_id=pinned_message.message_id,
        disable_notification=True,
    )
